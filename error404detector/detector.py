# coding: utf-8

from systemtools.basics import *
from systemtools.location import *
from systemtools.duration import *
from systemtools.system import *
from systemtools.file import *
from systemtools.logger import *
from datastructuretools.basics import *
from datastructuretools.hashmap import *
from datatools.htmltools import *
from datastructuretools.processing import *
from sklearn import svm
from sklearn import tree
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
import lxml.html
from bs4 import BeautifulSoup
from nlptools.tokenizer import *
from error404detector import __version__
from threading import Lock
import random

class Error404Detector:
    """
        If the dataset change, the
    """
    def __init__(self,
                 verbose=True,
                 logger=None,
                 dataDir=None,
                 modelDir=None,
                 cacheMax=10000,
                 pattern404="/*/404/*.html",
                 patternOk="/*/ok/*.html",
                 patternHash="/*/*/*.html"):
        # Misc:
        self.verbose = verbose
        self.logger = logger
        self.vocInitialized = False
        self.cacheLock = Lock()
        self.trainLock = Lock()
        self.initVoc()
        # Some processing cache:
        self.lowerHtmlCache = SerializableDict(funct=lower, limit=cacheMax)
        self.lowerHtml2TextCache = SerializableDict(funct=html2Text, limit=cacheMax)
        self.lowerTitleCache = SerializableDict(funct=htmlTitle, limit=cacheMax)
        self.tokenizedTitleCache = SerializableDict(funct=tokenize, limit=cacheMax)
        self.tokenizedTextCache = SerializableDict(funct=tokenize, limit=cacheMax)
        # All paths:
        self.dataDir = dataDir
        if self.dataDir is None:
            self.dataDir = getDataDir() + "/Misc/error404"
        self.modelDir = modelDir
        self.subDirName = "404detector"
        if self.modelDir is None:
            self.modelDir = tmpDir(subDir=self.subDirName)
        self.pattern404 = self.dataDir + pattern404
        self.patternOk = self.dataDir + patternOk
        self.patternHash = self.dataDir + patternHash
        # We use all these features:
        self.featuresFunctions = \
        [
            self.lengthFeatures,
            self.vocBowFeatures,
            self.vocCountFeatures,
            self.vocSubstractFeatures,
        ]
        # We get the hash and we set the model location
        # The hash will change (so the model will be re-trained)
        # when the version, or the dataset, or features are changed
        featureFunctionStr = ""
        for current in self.featuresFunctions:
            featureFunctionStr += current.__name__
        self.hash = hash \
        (
            str(sortedGlob(self.patternHash)) + \
            str(__version__) + \
            featureFunctionStr + \
            type(self.getPredictor()).__name__
        )
        self.modelPath = self.modelDir + "/model-" + self.hash + ".bin"
        # We train the model:
        self.model = None
        self.train()

    def getFeaturesFromPath(self, filePath):
#         print(filePath)
        html = fileToStr(filePath)
        result = self.getFeatures(html)
        return result

    def getFeatures(self, html):
        currentFeatures = []
        for currentFunct in self.featuresFunctions:
            currentFeatures += currentFunct(html)
        return currentFeatures

    def getTrainData(self):
        # We get all files:
        all404Files = sortedGlob(self.pattern404)
        allOkFiles = sortedGlob(self.patternOk)
        # We get all features:
        allLabels = [1] * len(all404Files) + [0] * len(allOkFiles)
        tp = Pool(mapType=MAP_TYPE.parmap) # best choice is parmap here
        tt = TicToc()
        tt.tic()
        allFeatures = tp.map(all404Files + allOkFiles, self.getFeaturesFromPath)
        tt.toc()
        return (allFeatures, allLabels)

    def getPredictor(self):
#         return tree.DecisionTreeClassifier() # 97
#         return svm.LinearSVC() # 69
        return ensemble.RandomForestClassifier() # 99
#         return naive_bayes.GaussianNB() # 87

    def crossValidation(self, k=20):
        clf = self.getPredictor()
        (allFeatures, allLabels) = self.getTrainData()
        scores = cross_val_score(clf, allFeatures, allLabels, cv=k, n_jobs=-1)
        scoreMean = scores.mean()
        log("Accuracy: %0.2f (+/- %0.2f)" % (scoreMean, scores.std() * 2), self)
        return scoreMean

    def crossValidationSeeFailed(self, k=20, openInFirefox=False):
        # We get the predictor:
        clf = self.getPredictor()
        # We get all features:
        (allFeatures, allLabels) = self.getTrainData()
        # We chunk all features (k-fold cross-validation):
        allFeaturesChunks = chunks(allFeatures, k)
        allLabelsChunks = chunks(allLabels, k)
        # And for all k-fold, we get failed elements in the test set:
        failsElementFeatures = []
        failsElementRatio = [0] * len(allFeaturesChunks)
        for i in range(len(allFeaturesChunks)):
            # We get features and labels of the test set:
            featuresTestSet = allFeaturesChunks[i]
            labelsTestSet = allLabelsChunks[i]
            # Now w get all k-1 features and labels:
            featuresTrainSet = []
            for u in range(len(allFeaturesChunks)):
                if u != i:
                    featuresTrainSet += allFeaturesChunks[u]
            labelsTrainSet = []
            for u in range(len(allLabelsChunks)):
                if u != i:
                    labelsTrainSet += allLabelsChunks[u]
            # We train with the train set:
            clf.fit(featuresTrainSet, labelsTrainSet)
            # For each element in the test set, we try to predict it:
            for u in range(len(featuresTestSet)):
                currentElementFeatures = featuresTestSet[u]
                currentElementLabel = labelsTestSet[u]
                prediction = clf.predict([currentElementFeatures])[0]
                # And we store it if the prediction is wrong:
                if currentElementLabel != prediction:
                    failsElementRatio[i] += 1
                    failsElementFeatures.append(currentElementFeatures)
            failsElementRatio[i] = (len(featuresTestSet) - failsElementRatio[i]) / len(featuresTestSet)
        # We get all files in the same order:
        all404Files = sortedGlob(self.pattern404)
        allOkFiles = sortedGlob(self.patternOk)
        allFiles = all404Files + allOkFiles
        allFailedFiles = []
        # We get failed files:
        for currentFail in failsElementFeatures:
            indexFail = allFeatures.index(currentFail)
            allFailedFiles.append(allFiles[indexFail])
        # And we print all failed files:
        allFailedFiles = list(set(allFailedFiles))
        printLTS(allFailedFiles)
        if openInFirefox:
            import sh
            for current in allFailedFiles:
                sh.firefox(current)
        # Now we compute the mean:
        print(sum(failsElementRatio)/len(failsElementRatio))

    def train(self):
        with self.trainLock:
            # Try to find an existing serialized model:
            if fileExists(self.modelPath):
                # Get the model from file system:
                log("Loading the model from the disk: " + self.modelPath, self)
                self.model = joblib.load(self.modelPath)
            # Else we train a new model and store it:
            elif isDir(self.dataDir):
                log("Training the model", self)
                # We first delete all previous files
                self.resetModel()
                # We get all features:
                (allFeatures, allLabels) = self.getTrainData()
                # We train the model:
                self.fit(allFeatures, allLabels)
                # We store the model
                log("Storing the model " + self.modelPath, self)
                joblib.dump(self.model, self.modelPath)
            else:
                logError("No model and no data found, you have to first train a model with data given on GitHub.", self)

    def fit(self, allFeatures, allLabels):
        clf = self.getPredictor()
        self.model = clf.fit(allFeatures, allLabels)

    def resetModel(self):
        deletePattern = tmpDir(subDir=self.subDirName) + "/model-*.bin"
        globRemove(deletePattern)


    def initVoc(self):
        # We first check if it was already init:
        if not self.vocInitialized:
            self.vocInitialized = True
            # On text lowered:
            voc1 = ["404", "error", "not found", "Moved Temporarily", "401 Unauthorized", "403 Forbidden", "Request Timeout", "Too Many Requests", "Service Unavailable", "oops!", "access denied", "Subscribe to read", "security check"]
#             voc1 = ["404", "error", "not found", "Moved Temporarily", "401 Unauthorized", "403 Forbidden", "Request Timeout", "Too Many Requests", "Service Unavailable", "404 ", " 404", "oops!"]
#             # On text lowered:
            voc2 = ["404 not found", "page not found", "Moved Temporarily", "401 Unauthorized", "403 Forbidden", "Request Timeout", "Too Many Requests", "Service Unavailable"]
            # On html lowered:
            voc3 = ["404<", ">404"]
            voc30 = ["404", "error"]
            # On tokenized text lowered:
            voc4 = ["found", "Requests", "Unavailable", "Service", "404", "error", "Unauthorized", "page", "Temporarily", "Timeout", "Forbidden", "403", "Moved", "not", "denied"]
            # On tokenized text lowered:
            voc5 = ["oops", "sorry", "apologies", "search", "page", "looking", "dead", "check", "cannot", "exists", "exist", "trouvée", "request", "matching"]
            # convert each in lower and sets:
            def convertAllVoc(allVoc):
                newAllVoc = []
                for voc in allVoc:
                    newVoc = []
                    for item in voc:
                        item = item.lower()
                        newVoc.append(item)
                    newVoc = list(set(newVoc))
                    newAllVoc.append(newVoc)
                return newAllVoc
            self.allTextLoweredVoc = convertAllVoc([
                                                    voc1,
#                                                     voc2,
                                                    ])
            self.allHtmlLoweredVoc = convertAllVoc([
                                                    voc3,
                                                    voc30,
                                                    ])
            self.allTokenizedTextLoweredVoc = convertAllVoc([
                                                            voc4,
                                                            voc5,
                                                             ])
            # Aggregate sames:
            def aggregateListOfList(allVoc):
                newAllVocAggregated = []
                for current in allVoc:
                    newAllVocAggregated += current
                return set(newAllVocAggregated)
            self.allTextLoweredVocAggregated = aggregateListOfList(self.allTextLoweredVoc)
            self.allHtmlLoweredVocAggregated = aggregateListOfList(self.allHtmlLoweredVoc)
            self.allTokenizedTextLoweredVocAggregated = aggregateListOfList(self.allTokenizedTextLoweredVoc)

    def getCachedData(self, html):
        """
            This method take a html str and parse it with caches structures
        """
        with self.cacheLock:
            html = self.lowerHtmlCache[html]
            text = self.lowerHtml2TextCache[html]
            title = self.lowerTitleCache[html]
            titleTokens = self.tokenizedTitleCache[title]
            textTokens = self.tokenizedTextCache[text]
            return (html, title, text, titleTokens, textTokens)

    def lengthFeatures(self, html):
        (html, title, text, titleTokens, textTokens) = self.getCachedData(html)
        features = []
        if title is None:
            features.append(0)
        else:
            features.append(len(title))
        features.append(len(html))
        features.append(len(text))
        return features

    def vocBowFeatures(self, html):
        (html, title, text, titleTokens, textTokens) = self.getCachedData(html)
        self.initVoc()
        features = []
        for (allVoc, source) in \
        [
#             # Here we check multiword voc in the text:
#             (self.allTextLoweredVoc, text),
#             # We check some html element in the html:
#             (self.allHtmlLoweredVoc, html),
#             # Next we check if these tokens exist in the tokenized text:
#             (self.allTokenizedTextLoweredVoc, textTokens),
            # And finally we check if these tokens exist in the tokenized title:
            (self.allTokenizedTextLoweredVoc, titleTokens),
        ]:
            for voc in allVoc:
                for word in voc:
                    if source is None or word not in source:
                        features.append(False)
                    else:
                        features.append(True)
        return features

    def vocCountFeatures(self, html):
        (html, title, text, titleTokens, textTokens) = self.getCachedData(html)
        self.initVoc()
        features = []
        for (allVoc, source) in \
        [
            # Here we check multiword voc in the text:
            (self.allTextLoweredVocAggregated, text),
            # We check some html element in the html:
            (self.allHtmlLoweredVocAggregated, html),
            # Next we check if these tokens exist in the tokenized text:
            (self.allTokenizedTextLoweredVocAggregated, textTokens),
            # And finally we check if these tokens exist in the tokenized title:
            (self.allTokenizedTextLoweredVocAggregated, titleTokens),
        ]:
            inter = intersection([allVoc, source])
            count = len(inter)
            features.append(count)
        return features

    def vocSubstractFeatures(self, html):
        (html, title, text, titleTokens, textTokens) = self.getCachedData(html)
        self.initVoc()
        features = []
        theVoc = self.allTokenizedTextLoweredVocAggregated
        features.append(len(listSubstract(titleTokens, theVoc)))
        features.append(len(listSubstract(textTokens, theVoc)))
        return features

    def autoTest(self):
        all404Files = sortedGlob(self.pattern404)
        allOkFiles = sortedGlob(self.patternOk)
        failedCount = 0
        for files, label in [(all404Files, 1), (allOkFiles, 0)]:
            for currentFile in files:
                prediction = self.is404(fileToStr(currentFile))
#                 prediction = is404Error(fileToStr(currentFile))
                if prediction != label:
                    failedCount += 1
                    print("Failed: " + currentFile)
        print("failedCount=" + str(failedCount))
        print("files count=" + str(len(all404Files + allOkFiles)))
        print("precision=" + str((len(all404Files + allOkFiles) - failedCount) / len(all404Files + allOkFiles)))


    def is404(self, html):
        return self.model.predict([self.getFeatures(html)])[0] == 1


def htmlTitle(html):
    soup = BeautifulSoup(html, "lxml")
    title = soup.title
    if title is not None:
        title = strip(title.string)
    return title








def is404Error(html, debug=False):
#     strToFile(html, getExecDirectory(__file__) + "/tmp/test.html")
#     exit()
    # If we found any of this in the first "<title(.*)</title>", it's a 404:
    match404Title = ["404", "error", "not found", "Moved Temporarily", "401 Unauthorized", "403 Forbidden", "Request Timeout", "Too Many Requests", "Service Unavailable", "404 ", " 404", "404 not found", "page not found", "404<", ">404", "Moved Temporarily", "401 Unauthorized", "403 Forbidden", "Request Timeout", "Too Many Requests", "Service Unavailable"]
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

if __name__ == '__main__':
    for current in sortedGlob(dataDir() + '/Misc/error404/*/*/*.html'):
        print(current)
        print(fileToStr(current)[0:10])










