# coding: utf-8

from systemtools.basics import *
from systemtools.location import *
from systemtools.system import *
from systemtools.file import *
from systemtools.logger import log, logInfo, logWarning, logError, Logger
from sklearn import tree

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
        
        
        
        all404Files = sortedGlob(self.pattern404)
        allOkFiles = sortedGlob(self.patternOk)
        
#         printLTS(sortedGlob(self.patternOk))
#         printLTS(sortedGlob(self.patternHash))
        
#         logInfo("blabla", self)
        
        self.model = None
#         self.train()
        
        
    def train(self):
        
        # We get the hash:
        hashPath = self.dataLocation + "/models/" + "model-hash.txt"
        theHash = hash(str(sortedGlob(self.dataLocation + "/*/*.html")))
        
        # Try to find an existing serialized model:
        if fileToStr(hashPath) == theHash:
            # Get the model from file system:
            self.model = None
        else:
        
        
        
        
            # Else we train a model and we serialize it:
            
    #         X = [[0, 0], [1, 1]]
    #         Y = [0, 1]
    #         clf = tree.DecisionTreeClassifier()
    #         clf = clf.fit(data, labels)
    #         return clf
    
            
            # We store the model
            
            # We store the hash of all files trained
            
            
            strToFile(theHash, hashPath)
            
            self.model = None


            
    def is404(self, html):
        return True
    
    
    
    def getFeatures(self, html):
        features = []
        features.append(len(html))
        return features

    def crossValidation(self):
        
        # We don't care overfitting but you can try to display the tree
        
        return 0.5


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
        
    