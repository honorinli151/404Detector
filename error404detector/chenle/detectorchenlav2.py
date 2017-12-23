# -*- coding:utf-8 -*-

# Attetion, il faut preciser les paths 'datalocation', il faut etre sur les entree sont sou forme html
from systemtools.basics import *
from systemtools.location import *
from systemtools.system import *
from systemtools.file import *
from systemtools.logger import log, logInfo, logWarning, logError, Logger
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import pandas as pd
import sklearn as skn
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import re
import os
import numpy as np
import nltk
from nltk import word_tokenize

'''
Modified by Chenle Li, Nov 23 2017
'''

# Attention the train must be all tagged. And the mode test is because the author did not get the right to create a file in the default datalocation.
class Error404Detector:
    def __init__(self,
                 verbose=True,
                 logger=None,
                 dataLocation=None,
                 pattern404="/*/404/*.html",
                 patternOk="/*/ok/*.html",
                 patternHash="/*/*/*.html",
                 mode=None):
        self.verbose = verbose
        self.logger = logger
        self.dataLocation = dataLocation
        if self.dataLocation is None:
            self.dataLocation = dataDir() + '/Misc/error404'
        self.pattern404 = self.dataLocation + pattern404
        self.patternOk = self.dataLocation + patternOk
        self.patternHash = self.dataLocation + patternHash
        self.model = None
        self.cross_validation_score = 0
        self.mode = mode
        self.features = None
        self.train_df = None

    def train(self):

        # We get the hash:
        if self.mode == 'test':
            hashPath = "/home/student/parcours-recherche/model/model-hash.txt"
        else:
            hashPath = self.dataLocation + "/model/" + "model-hash.txt"
        theHash = hash(str(sortedGlob(self.dataLocation + "/*/*.html")))

        # Try to find an existing serialized model:
        if os.path.exists(hashPath) and fileToStr(hashPath) == theHash:
            if self.mode == 'test':
                self.model = joblib.load("/home/student/parcours-recherche/model/404detectormodel.m")
            # Get the model from file system:
            else:
                self.model = joblib.load(self.dataLocation + '/model/404detectormodel.m')
            print('Already trained')
        else:
            # Else we stock the hash
            strToFile(theHash, hashPath)
            # data process
            self.train_df = pd.DataFrame(clean_objet(sortedGlob(self.patternOk)+sortedGlob(self.pattern404)))
            self.features = feature_generator(self.train_df)
            # data treatment
            clf = DecisionTreeClassifier()
            # We store the model
            self.cross_validation_score = cross_val_score(clf, self.features, self.train_df['type']).mean()
            print(self.cross_validation_score)
            clf = clf.fit(self.features, self.train_df['type'])
            self.model = clf
            if self.mode == 'test':
                joblib.dump(clf, "/home/student/parcours-recherche/model/404detectormodel.m")
            else:
                joblib.dump(clf, self.dataLocation + "/model/404detectormodel.m")
            print('New data trained')

    # We apply the model actuel to predict the html that we want
    def is404(self, htmlloc):
        if type(htmlloc) == str:
            htmlloc = [htmlloc]
        train_df = clean_objet(htmlloc)
        features = feature_generator(train_df)
        clf = self.model = joblib.load("/home/student/parcours-recherche/model/404detectormodel.m")
        train_df['prediction'] = pd.Series(clf.predict(features), index=train_df.index)
        print(train_df[['path', 'prediction']])
        return train_df

    # Get the dataframe-like feature of one html.
    def getFeatures(self, html):
        return feature_generator(html)

    def crossValidation(self):

        # We don't care overfitting but you can try to display the tree

        return self.cross_validation_score


def is404Error(html, debug=False):
#     strToFile(html, getExecDirectory(__file__) + "/tmp/test.html")
#     exit()
    # If we found any of this in the first "<title(.*)</title>", it's a 404:
    match404Title = ["404", "error", "not found", "Moved Temporarily", "401 Unauthorized", "403 Forbidden", "Request Timeout", "Too Many Requests", "Service Unavailable", "404 ", " 404"]
    titleResult = re.finditer("<title(.*)</title>", html, re.DOTALL)
    if titleResult is None:
        return True
    titleResult = list(titleResult)
    if len(titleResult) == 0:
        return True
    title = None
    for current in titleResult:
        title = current.group(1)
        if title is None:
            return True
        if len(title) >= 1:
            title = title[1:]
        title = title.lower()
        break
    for current in match404Title:
        if current.lower() in title:
            if debug:
                print(">>>>> " + current)
            return True
    # Or if any of this is in the body:
    match404Body = ["404 not found", "page not found", "404<", ">404", "Moved Temporarily", "401 Unauthorized", "403 Forbidden", "Request Timeout", "Too Many Requests", "Service Unavailable"]
    htmlLower = html.lower()
    for current in match404Body:
        if current.lower() in htmlLower:
            if debug:
                print(">>>>> " + current)
            return True
    # Else we return True
    return False


def test():
    pass

if __name__ == '__main__':
    logger = Logger("Error404Detector.log")

    currentInstance = Error404Detector(logger=logger)


'''
Modified by Chenle Li, Dec 19 2017
'''

list_key = ['oops', 'oops!', 'sorry','apologies','search', 'page', 'looking', 'dead', 'check', 'cannot', 'exists', 'exist', 'trouvée', 'request', 'matching', 'unavailable']
# Generate features from the list(two patterns) or a single html
def feature_generator(dataframe):
    length_dict = feature_length(dataframe)
    presence_dict = feature_wordspresence(dataframe)
    word_gen_dict = feature_num_word_general(dataframe)
    features = dict(presence_dict, **length_dict)
    #features = dict(features, **word_gen_dict)
    #features = presence_dict.copy().update(length_dict)
    features_df = pd.DataFrame.from_dict(features, orient='index').transpose()
    return features_df

# We determine the word presence of 404error keywords, and we care about the difference between bode and title
def feature_wordspresence(dataframe):
    presence = {}
    for key in list_key:
        presence[key+'title'] = []
        presence[key+'body'] = []
    for row in dataframe.itertuples():
        for key in list_key:
            if key in row[1].split():
                presence[key+'title'].append(True)
                #print(key in row[1])
                #print(key in row[2])
            if key in row[2].split():
                presence[key+'body'].append(True)
            if not(key in row[2].split()):
                presence[key+'body'].append(False)
            if not(key in row[1].split()):
                presence[key+'title'].append(False)
    return presence

# Calculation of the length of titles and bodies
def feature_length(dataframe):
    length_title = []
    length_body = []
    for row in dataframe.itertuples():
        #print(row)
        length_title.append(len(row[3]))
        length_body.append(len(row[1]))
    return {'lengthbody': length_body, 'lengthtitle': length_title}

# We define here num_word_general = number of words in the whole page - numbers of keywords in the page
def feature_num_word_general(dataframe):
    title_True = []
    body_True = []
    title_False = []
    body_False = []
    for row in dataframe.itertuples():
        if row[3] == False:
            title_False.append(count_num_word_general(row[1]))
            body_False.append(count_num_word_general(row[2]))
        elif row[3] == True:
            title_True.append(count_num_word_general(row[1]))
            body_True.append(count_num_word_general(row[2]))
    return {'wordgen_title': title_True+title_False, 'wordgen_body': body_True+body_False}

# Define count_num_word_genaral
def count_num_word_general(string):
    words = string.split()
    length = len(words)
    count = 0
    for word in words:
        if word in list_key:
            count += 1
    if length != 0:
        re = (length - count)/length
    else:
        re = 0
    return re

# Remove all the tags, scripts in one html
def clean_html(html):
    soup = bs(html)
    try:
        title = soup.title.contents[0]
    except (AttributeError, IndexError):
        title = ''
    for s in soup(['script','style']):
        s.decompose()
    return ' '.join(soup.stripped_strings).lower(), title.lower()

# Clean all the html in the folder
def clean_objet(listhtml):  # We need the order [patternok, pattern404]
    train = []
    if len(listhtml) == 1:
        temp = {}
        temp['body'], temp['title'] = clean_html(open(listhtml[0]))
        temp['path'], temp['type'] = listhtml[0], 'False'
        train_df = pd.DataFrame([temp])
        return train_df
    if len(listhtml) > 1:
        for html_path in listhtml:
            #print(html)
            #print(html_path)
            temp = {}
            temp['body'], temp['title'] = clean_html(open(html_path))
            temp['type'] = trueorfalse(html_path)
            temp['path'] = html_path
            train.append(temp)
    # train_df = pd.DataFrame(train, columns=['title', 'body', 'type'])
    return train

def trueorfalse(html_path):
    if 'ok' in html_path:
        return True
    elif '404' in html_path:
        return False
    else:
        return False