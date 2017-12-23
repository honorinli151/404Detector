# coding: utf-8

from systemtools.basics import *
from systemtools.location import *
from systemtools.system import *
from systemtools.file import *
from systemtools.logger import log, logInfo, logWarning, logError, Logger
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import pandas as pd
import sklearn as skn
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

# Attetion the train must be all tagged.
class Error404Detector:
    def __init__(self,
                 verbose=True,
                 logger=None,
                 dataLocation=None,
                 pattern404="/*/404/*.html",
                 patternOk="/*/ok/*.html",
                 patternHash="/*/*/*.html"):
        self.verbose = verbose
        self.logger = logger
        self.dataLocation = dataLocation
        if self.dataLocation is None:
            self.dataLocation = dataDir() + "/Misc/error404"
        self.pattern404 = self.dataLocation + pattern404
        self.patternOk = self.dataLocation + patternOk
        self.patternHash = self.dataLocation + patternHash
#         printLTS(sortedGlob(self.pattern404))
#         printLTS(sortedGlob(self.patternOk))
#         printLTS(sortedGlob(self.patternHash))

#         logInfo("blabla", self)

        self.model = None
        self.cross_validation_score = 0
#         self.train()


    def train(self):

        # We get the hash:
        hashPath = self.dataLocation + "/models/" + "model-hash.txt"
        theHash = hash(str(sortedGlob(self.dataLocation + "/*/*.html")))

        # Try to find an existing serialized model:
        if False: #fileToStr(hashPath) == theHash:
            # Get the model from file system:
            self.model = None
        else:
            # Else we train a model and we serialize it:

    #         X = [[0, 0], [1, 1]]
    #         Y = [0, 1]
    #         clf = tree.DecisionTreeClassifier()
    #         clf = clf.fit(data, labels)
    #         return clf

            # data process
            train_df = clean_objet(datalocationtest)
            features_df = feature_generator(train_df)
            # data treatment
            clf = DecisionTreeClassifier()
            # We store the model

            # We store the hash of all files trained

            strToFile(theHash, hashPath)

            print(features_df)
            exit()
            self.model = clf.fit(features_df, train_df['type'])
            self.cross_validation_score = cross_val_score(clf1, features_df, train_df['type'])


    # We apply the model actuel to predict the html that we want
    def is404(self, html):
        features = feature_generator(html)
        return self.model.predict(features)

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
Added by Chenle Li, Nov 23 2017
'''

# Generate features from the list(two patterns) or a single html
def feature_generator(dataframe):
    length_dict = feature_length(train_df)
    presence_dict = feature_wordspresence(train_df)
    features = dict(presence_dict, **length_dict)
    features_df = pd.DataFrame(features)
    return features_df

# We determine the word presence of 404error keywords, and we care about the difference between bode and title
def feature_wordspresence(dataframe):
    list_key = ["404", "error", "not found",  "401 Unauthorized", "403 Forbidden", "Request Timeout"]
    presence = {}
    for key in list_key:
        presence[key+'title'] = []
        presence[key+'body'] = []
    for row in dataframe.itertuples():
        for key in list_key:
            if key in row[1].lower():
                presence[key+'title'].append(True)
                #print(key in row[1])
                #print(key in row[2])
            if key in row[2].lower():
                presence[key+'body'].append(True)
            if not(key in row[2].lower()):
                presence[key+'body'].append(False)
            if not(key in row[1].lower()):
                presence[key+'title'].append(False)
    return presence

# Calculation of the length of titles and bodies
def feature_length(dataframe):
    length_title_True = []
    length_body_True = []
    length_title_False = []
    length_body_False = []
    for row in dataframe.itertuples():
        #print(row)
        if row[3] == False:
            length_title_False.append(len(row[1]))
            length_body_False.append(len(row[2]))
        elif row[3] == True:
            length_title_True.append(len(row[1]))
            length_body_True.append(len(row[2]))
        elif row[3] == 'NaN':
            return {'lengthtitle': length_title_True.append(len(row[1])), 'lengthbody': length_body_True.append(len(row[2]))}
    return {'lengthbody': length_body_True+length_body_False, 'lengthtitle': length_title_True+length_title_False}

# Remove all the tags, scripts in one html
def clean_html(html):
    soup = bs(html)
    try:
        title = soup.title.contents[0]
    except (AttributeError, IndexError):
        title = ''
    for s in soup(['script','style']):
        s.decompose()
    return ' '.join(soup.stripped_strings), title

# Clean all the html in the folder
def clean_objet(htmlorfolders):  # We need the order [patternok, pattern404]
    train = []
    if os.path.isfile(htmlorfolders):
        temp = {}
        temp['body'], temp['title'] = clean_html(open(htmlorfolders))
        temp['path'], temp['type'] = htmlorfolders, 'NaN'
        train_df = pd.DataFrame([temp], columns['title', 'body', 'type'])
    if os.path.isdir(htmlorfolders):
        for html_part in os.listdir(htmlorfolders):
            #print(html_part)
            if not html_part.startswith('.'):
                if html_part == 'ok':
                    mark = True
                elif html_part == '404':
                    mark = False
                else:
                    mark = 'NaN'
                html_part_path = html_folder+html_part
                for html in os.listdir(html_part_path):
                    html_path = html_part_path+"/"+html
                    #print(html_path)
                    temp = {}
                    temp['body'], temp['title'] = clean_html(open(html_path))
                    temp['type'] = mark
                    temp['path'] = html_part+html
                    train.append(temp)
    train_df = pd.DataFrame(train, columns=['title', 'body', 'type'])
    return train_df

if __name__ == '__main__':
    e = Error404Detector()
    e.train()