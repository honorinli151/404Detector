# coding: utf-8

from systemtools.basics import *
from systemtools.location import *
from systemtools.system import *
from systemtools.file import *
from systemtools.logger import *
from datastructuretools.basics import *
from sklearn import tree
from sklearn.externals import joblib
import html2text

class Error404Detector:
    """
        If the dataset change, the
    """
    def __init__(self,
                 verbose=True,
                 logger=None,
                 dataDir=None,
                 modelDir=None,
                 pattern404="/*/404/*.html",
                 patternOk="/*/ok/*.html",
                 patternHash="/*/*/*.html"):
        # Misc:
        self.verbose = verbose
        self.logger = logger
        # Some cache:
        self.html2textCache = CacheDict(html2text.html2text, 30)
        self.titleCache = CacheDict(htmlTitle, 30)
        # All paths:
        self.dataDir = dataDir
        if self.dataDir is None:
            self.dataDir = dataDir() + "/Misc/error404"
        self.modelDir = modelDir
        self.subDirName = "404detector"
        if self.modelDir is None:
            self.modelDir = tmpDir(subDir=self.subDirName)
        self.pattern404 = self.dataDir + pattern404
        self.patternOk = self.dataDir + patternOk
        self.patternHash = self.dataDir + patternHash
        # We get the hash and we set the model location:
        self.hash = hash(str(sortedGlob(self.patternHash)))
        self.modelPath = self.modelDir + "/model-" + self.hash + ".bin"
        # We train the model:
        self.model = None
        self.train()

    def getAllFeatures(self):
        # We get all files:
        all404Files = sortedGlob(self.pattern404)
        allOkFiles = sortedGlob(self.patternOk)
        filesAndLabels = []
        for file in all404Files:
            filesAndLabels.append((file, 1))
        for file in allOkFiles:
            filesAndLabels.append((file, 0))
        # We get all features:
        featuresFunctions = \
        [
            self.lengthFeatures
        ]
        allFeatures = []
        allLabels = []
        for (file, label) in filesAndLabels:
            html = fileToStr(file)
            currentFeatures = []
            for currentFunct in featuresFunctions:
                currentFeatures += currentFunct(html)
            allFeatures.append(currentFeatures)
            allLabels.append(label)
        return (allFeatures, allLabels)

    def crossValidation(self):
        # http://scikit-learn.org/stable/modules/cross_validation.html
        n_jobs=-1

        cross_val_score(clf, iris.data, iris.target, cv=20)

        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    def train(self):
        # Try to find an existing serialized model:
        if fileExists(self.modelPath):
            # Get the model from file system:
            log("Loading the model from the disk: " + self.modelPath, self)
            self.model = joblib.load(self.modelPath)
        # Else we train a new model and store it:
        elif isDir(self.dataDir):
            log("Training the model", self)
            # We first delete all previous files
            deletePattern = tmpDir(subDir=self.subDirName) + "/model-*.bin"
            globRemove(deletePattern)
            # We get all features:
            (allFeatures, allLabels) = self.getAllFeatures()
            # We train the model:
            self.fit(allFeatures, allLabels)
            # We store the model
            log("Storing the model " + self.modelPath, self)
            joblib.dump(self.model, self.modelPath)
        else:
            logError("No model and no data found, you have to first train a model with data given on GitHub.", self)

    def fit(self, allFeatures, allLabels):
        clf = tree.DecisionTreeClassifier()
        self.model = clf.fit(allFeatures, allLabels)

    def lengthFeatures(self, html):
        features = []
        title = self.titleCache[html]
        if title is None:
            features.append(0)
        else:
            features.append(len(title))
        features.append(len(html))
        features.append(len(self.html2textCache[html]))

    def is404(self, html):
        return True



    def getFeatures(self, html):
        features = []
        features.append(len(html))
        return features

    def crossValidation(self):

        # We don't care overfitting but you can try to display the tree

        return 0.5





def htmlTitle(html):
    titleResult = re.finditer("<title(.*)</title>", html, re.DOTALL)
    if titleResult is None:
        return None
    titleResult = list(titleResult)
    if len(titleResult) == 0:
        return None
    title = None
    for current in titleResult:
        title = current.group(1)
        if title is None:
            return True
        if len(title) >= 1:
            title = title[1:]
        title = title.lower()
        break
    return title






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

