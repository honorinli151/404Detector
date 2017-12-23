# coding: utf-8


########## WORSPACE IN PYTHON PATH ##########
# Include all Paths :
# TODO faire un include de tous les sous dossiers du Workspace en remontant 4 dossiers
# TODO (mettre une variable pour le nombre de dossier a remonter).
# TODO mettre aussi le changement en utf-8
# TODO Et mettre le os.chdir("??") aussi
# TODO Faire une sorte d'entete pour chaque fichier python
# Updated 09/03/17
workspaceName = "WebCrawler" # Set the name of the Workspace in all ancestors folders
onlyInit = False # TODO
import sys
import os
import re
def dirsHasRegex(dirs, regex):
    if not isinstance(dirs, list):
        dirs = [dirs]
    # for all subdirs:
    for currentDir in dirs:
        # We get all files:
        files = getFileNames(currentDir)
        # We check if there .py or __init__.py:
        for fname in files:
            if re.search(regex, fname) is not None:
                return True
    return False

def getFileNames(currentFolder):
    files = [item for item in os.listdir(currentFolder) if os.path.isfile(os.path.join(currentFolder, item))]
    return files

def getSubdirsPaths(currentFolder):
    dirs = [currentFolder + item + "/" for item in os.listdir(currentFolder) if os.path.isdir(os.path.join(currentFolder, item))]
    return dirs

# We get the Workspace dir:
currentFolder = os.path.dirname(os.path.abspath(__file__))
workspace = currentFolder.split(workspaceName)[0] + workspaceName + "/"
# And while there are folders to watch:
penddingFolderList = [workspace]
pathsToAdd = []
while len(penddingFolderList) != 0:
    # We pop the current folder in in the pending queue:
    currentFolder = penddingFolderList.pop(0)
    if not currentFolder.split("/")[-2].startswith("."):
        hasPy = dirsHasRegex(currentFolder, ".py$")
        atLeastOneSubDirHasInit = dirsHasRegex(getSubdirsPaths(currentFolder), "__init__.py")
        # We add it in the path list:
        if hasPy or atLeastOneSubDirHasInit:
            pathsToAdd.append(currentFolder)
        # And We add the subfolders in the pending queue if there is no __init__.py:
        if not atLeastOneSubDirHasInit:
            subDirs = getSubdirsPaths(currentFolder)
            penddingFolderList += subDirs
# We add all paths in the python path:
print(pathsToAdd)
for path in pathsToAdd:
    sys.path.append(path)
#     print path
#############################################


import pymongo
from databasetools.mongo import *
from systemtools.file import *
from systemtools.location import *
from systemtools.basics import *
from systemtools.hayj import *
from datatools.json import *
from datatools.csvreader import *
from webcrawler.crawler import *
from webcrawler.utils import *
from webcrawler.browser import *
from webcrawler.error404.urls import *
import sh
from webcrawler.error404.urls import *
import random
from webcrawler.error404.alreadydone import *
from systemtools.logger import log, logInfo, logWarning, logError, Logger

def testUrlParsing():
    printLTS(alreadyDone)



def listNews404():
    filePath = dataDir() + "/Misc/news-website-list/data/list.csv"
    outputDir404 = dataDir() + "/Misc/error404/from-newslist/404-test"
    jr = CSVReader(filePath)
    urlParser = URLParser()
    error404List = []
    for current in jr:
        urlParse = urlParser.parse(current["url"])
        url = urlParse.scheme + "://" + urlParse.netloc + "/aaaaaa"
        error404List.append(url)

#     error404List = error404List[0:3]

    printLTS(error404List)

#     exit()

    def crawlingCallback(data, browser=None):
        filePath = outputDir404 + "/" + getRandomStr() + ".html"
        html = data["html"]
        strToFile(html, filePath)

    def terminatedCallback(urlsFailedNotEnough, urlsFailedEnough):
        logInfo("urlsFailedNotEnough:")
        logInfo(listToStr(urlsFailedNotEnough))
        logInfo("urlsFailedEnough:")
        logInfo(listToStr(urlsFailedEnough))


    crawler = Crawler \
    (
        error404List,
        paramsDomain = \
        {
            "proxyInstanciationRate":
            {
                "alpha": [0.99],
                "beta": [NormalizedLawBeta.LOG]
            },
            "browserCount": [10],
            "parallelRequests": [10],
        },
        proxiesPath=dataDir() + "/Misc/" + "proxies-prod.txt",
        crawlingCallback=crawlingCallback,
        terminatedCallback=terminatedCallback,
        browsersVerbose=True,
        browsersDriverType=DRIVER_TYPE.chrome,
        banditRoundDuration=0, # 500
        stopCrawlerAfterSeconds=20,
        maxRetryFailed=2,
        ajaxSleep=3.0,
        browserMaxDuplicatePerDomain=8,
        useProxies=True,
        loadImages=True,
        browsersHeadless=isHostname("datasc"),
    )
    crawler.start()

#     proxies = getProxies(dataDir() + "/Misc/" + "proxies-test.txt")
#     printLTS(proxies)
#     b = Browser(proxy=random.choice(proxies), driverType=DRIVER_TYPE.chrome)
#
#     for url in error404List:
#         html = b.html(url)
#         printLTS(html)



def listNews():
    filePath = dataDir() + "/Misc/news-website-list/data/list.csv"
    outputDir404 = dataDir() + "/Misc/error404/from-newslist/404"
    outputDirOK = dataDir() + "/Misc/error404/from-newslist/ok"
    jr = CSVReader(filePath)
    urlParser = URLParser()
    error404List = []
    okList = []
    for current in jr:
        url = urlParser.normalize(current["url"])
        okList.append(url)
        error404List.append(url + "/jhgsdyuvsfd")

    random.shuffle(okList)
#     okList = listSubstract(okList, alreadyDone)
#     okList = listSubstract(okList, exclude)
#     okList = listSubstract(okList, ["http://nypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city/", "http://abcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532"])
    printLTS(okList)
#     printLTS(alreadyDone)
    input()
#     exit()
    random.shuffle(error404List)
    b = Browser(driverType=DRIVER_TYPE.chrome)
#     b = Browser(driverType=Browser.DRIVER_TYPE.chrome)
    iterList = [(okList, outputDirOK), (error404List, outputDir404)]

    error404List = toDO

    iterList = [(error404List, outputDir404)]
    for theList, path in iterList:
        for url in theList:
            if url not in alreadyDone and url not in exclude:
                filePath = path + "/" + getRandomStr() + ".html"
                toPrint = filePath + " ==> " + url[15:]
#                 print(toPrint)
                data = b.html(url)
#                 if data["status"] == REQUEST_STATUS.timeoutWithContent \
#                 or data["status"] == REQUEST_STATUS.success \
#                 or data["status"] == REQUEST_STATUS.error404:
                html = data["html"]
                strToFile(html, filePath)


def testFail():
    urls = ["http://nypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city/", "http://abcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532"]
    b = Browser(driverType=Browser.DRIVER_TYPE.chrome,
                useTimeoutGet=True,
                pageLoadTimeout=10)
    for url in urls:
        print(b.html(url)["title"])

taonews = None
def storeTaonews():
    (user, password, host) = (None, None, None)
    taonews = MongoCollection \
    (
        "crawling",
        "taonews",
        user=user,
        password=password,
        host=host,
    )
    print(taonews.size())

    outputDir404 = dataDir() + "/Misc/error404/from-taonews/404"
    outputDirOK = dataDir() + "/Misc/error404/from-taonews/ok"

    for thelist, outputPath in [(urlError404, outputDir404), (urlNotError404, outputDirOK)]:
        for current in thelist:
            result = taonews.findOne({"expanded_url": current})
            if result is None or len(result["html"]) < 10:
                print("fail")
                exit()
            strToFile(result["html"], outputPath + "/" + getRandomStr() + ".html")








if __name__ == '__main__':
#     printLTS(alreadyDone_old)
#     print(len(alreadyDone))
#     listNews404()
#     testUrlParsing()
#     testFail()

    storeTaonews()




    # FAIL sur bcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532
    # FAIL sur ypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city/

    # C'est le get qui foire tout, le timeout ne se lance pas

    # fail = ["http://nypost.com/2017/10/07/inside-the-mean-girls-culture-that-destroyed-sex-and-the-city/", "http://abcnews.go.com/Entertainment/wireStory/resignations-fallout-grow-embattled-producer-weinstein-50351532"]







