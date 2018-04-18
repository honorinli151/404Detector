# @Author: lichenle
# @Date:   2018-4-7 20:50:56
# @Email:  chenle.li@student.ecp.fr
# @Filename: Test package.py
# @Last modified by:   lichenle
# @Last modified time: 2018-4-18 23:29:42

# coding: utf-8

import os
import threading
from pymongo import MongoClient
from webcrawler.crawler import *
from databasetools.mongo import *
from lcdatatools import proxyfromtxt
from bs4 import BeautifulSoup


# def addToTheDatabasecrawl(data):
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client.news_stock
#     db.error404.insert_one(data)

# def crawlingCallback(data, browser=None):
#     global logger
#     try:
#         url = data["html"]
#         status = data["status"]
#         # If the request succeeded, we store it in a database:
#         if status in [REQUEST_STATUS.success, REQUEST_STATUS.timeoutWithContent]:
#             data = dictToMongoStorable(data)
#             addToTheDatabasecrawl(data)
#         # Else if the request succeeded but we got a 404:
#         elif status in [REQUEST_STATUS.error404]:
#             logError(url + " is a 404...", logger)
#     except Exception as e:
#         logException(e, logger, location="crawlingCallback")

def newsDataHas(url):
    global newscrawlCollction
    return newscrawlCollection.has({"url": url})

def addToTheDatabasecrawl(data):
    global newscrawlCollection
    try:
        # db.error404.insert_one(data)
#         if not newsDataHas(url):
        newscrawlCollection.insert(data)
    except Exception as e:
        logException(e, logger, location="addToTheDatabasecrawl")


# def crawlingCallback(data, browser=None):
#     global logger
#     try:
#         url = data["html"]
#         status = data["status"]
#         # If the request succeeded, we store it in a database:
#         if status in [REQUEST_STATUS.success, REQUEST_STATUS.timeoutWithContent]:
#             data = dictToMongoStorable(data)
#             addToTheDatabasecrawl(data)
#         # Else if the request succeeded but we got a 404:
#         elif status in [REQUEST_STATUS.error404]:
#             logError(url + " is a 404...", logger)
#     except Exception as e:
#         logException(e, logger, location="crawlingCallback")


def crawlingCallback(data, browser=None):
    global logger
    global crawler
    global counts
    global domains
    global u
    try:
        url = data["url"]
        status = data["status"]
        html = data["html"]
#         print(html)
        # If the request succeeded, we store it in a database if not done:
        if status in [REQUEST_STATUS.success, REQUEST_STATUS.timeoutWithContent]:
#             u = URLParser()
            domain_temp = u.getDomain(url)
            # print(domain_temp)
            if domain_temp in domains:
                if not newsDataHas(url):
                    data = dictToMongoStorable(data)
                    addToTheDatabasecrawl(data)
                    # print("Added to MongoDB")
#                     print(counts[domain_temp])
                # Check the counter
#                     if domain_temp in counts:
                    if counts[domain_temp] < 200:
                        # print("Entered begin bs4")
                        urls = getUrl(html, url)
                        if len(urls) > 0:
                            print("urls got")
#                         print(urls)
                        for url_a in urls:
                            if checkDomain(url_a, url):
                                if counts[domain_temp] < 200:
                                    crawler.put(url_a)
                                    # print("Put Finished")
                                    counts[domain_temp] += 1
#                                     crawler.stop()
                                    # print(counts[domain_temp])
                                    # print(url_a+"Added")
                                elif counts[domain_temp] >= 200:
                                    logInfo(domain + 'Full Charged!')
                                    break
                                    # print(domain_temp+"Over!")
#                                     crawler.stop()
#                     elif not domain_temp in counts:
#                         counts[domain_temp] = 1
#                     print("Counted")
                elif newsDataHas(url):
                    print('AlreadyGot')
#             print(counts)
#             crawler.stop()
        # Else if the request succeeded but we got a 404:
        elif status in [REQUEST_STATUS.error404]:
            # print("404")
#             crawler.stop()
            logError(url + " is a 404...", logger)
    except Exception as e:
#         crawler.stop()
        logException(e, logger, location="crawlingCallback")


def terminatedCallback(urlsFailedNotEnough, urlsFailedEnough):
    global logger
    for text, currentFailed in [("urlsFailedNotEnough", urlsFailedNotEnough), ("urlsFailedEnough", urlsFailedEnough)]:
        currentFailedText = ""
        for current in currentFailed:
            currentFailedText += str(current.data) + "\n"
        logInfo(text + ":\n" + currentFailedText, logger)


def getHtml(url, site):
    # global site
    client = MongoClient('mongodb://localhost:27017/')
    db = client.news_stock
    return db[site].find_one({'url': url})['html']


def checkDomain(url, site):
    # global site
    global u
    # u = URLParser()
    return True if u.getDomain(url) == u.getDomain(site) else False


def getUrl(html, url):
    global u
#     if urlParserSingleton is None:
#         urlParserSingleton = URLParser()
#     print('Getting Urls')
    soup = BeautifulSoup(html, "html.parser")
#     print("Soup Ready")
    urls = []
    try:
        for link in soup.find_all("a"):
#             print('Links')
            href = link.get('href')
            href = u.join(url, href)
#             urls.append(href)
            if checkDomain(href, url):
                urls.append(href)
    except Exception as e:
        print(str(e)+'getUrl')
    return urls

# def checkDomain(url, site):
#     # global site
#     global u
# #     u = URLParser()
#     return True if u.getDomain(url) == u.getDomain(site) else False

# def check_mongodb(crawler):
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client.news_stock
#     if db.error404.count() > 4:
#         print("Over clapped!")
#         crawler.stop()
# t.cancel()


# class NewsCrawlerGenerator:
#     def __init__(self, logger=None, max=200, url=None):
#         self.max = max
#         self.url = url
#
#     def urlsGen(self):
#         urls = [self.url]
#         for url in urls:
#             while len(urls) < self.max:
#                 urls.append(getUrl(getHtml(url, self.url), self.url))
#             else:
#                 break
#         print(str(len(urls))+'for'+site)
#         return urls


# if name == '__main__':
# test = input("Local Spider Lauching, enter 'I know' \
# to Start the Spider")
# if test != 'I know':
#     print('Quiting')
#     os._exit()
# chromdriver = "/Users/lichenle/Downloads/chromedriver"
# os.environ["webdriver.chrome.driver"]=chromdriver
# params = {"chromeDriverPath": "/Users/lichenle/Desktop/Untitled Folder\
# /chromedriver"}
# proxylist = [{"ip": "107.150.70.6", "port": "80", "user": "octopeek",\
#  "password": "librepost"}]
# crawler = Crawler(["https://www.yahoo.com/news/"], \
# browserUseFastError404Detection=True, crawlingCallback=crawlingCallback,
# proxies=proxylist, browserParams = params, logger=Logger("/Users/lichenle
# /Desktop/Untitled Folder/test.log"))
# # t = threading.Timer(60, check_mongodb(crawler))
# crawler.start()

# Custormize Parameters
# dir_name = os.path.dirname(__file__)
# proxytxtPath = os.path.join(dir_name, 'proxies.txt')  # A txt required
# sitestxtPath = os.path.join(dir_name,  '/sites.txt')
# loggerPath = os.path.join(dir_name, '/test.log')
# # sitestxtPath = '/Users/lichenle/Desktop/Untitled Folder/sites.txt'  # txt required
# # loggerPath = "/Users/lichenle/Desktop/Untitled Folder/test.log"
# dbName = news_stock
# collectionName = error404
# proxylist = proxyfromtxt(proxytxtPath, save_dict=True)
# sites = [line.rstrip('\n') for line in open(sitestxtPath)]
# u = URLParser()
# domains = [u.getDomain(site) for site in sites]
# counts = dict((domain, 0) for domain in domains)
# params = {"chromeDriverPath": os.path.join(dir_name, '/chromedriver')}
# newscrawlCollection = MongoCollection\
# (
#     dbName,
#     collectionName,
#     indexOn=["url"],
#     indexNotUniqueOn=["lastUrlDomain"],
#     # user=user, password=password, host=host,
#     version=newsCrawlerVersion,
#     giveHostname=True,
#     giveTimestamp=True,
#     logger=logger,
# )
#
# # Test Params
#
# # Initialize Crawler
# crawler = Crawler\
# (
#     sites,
#     proxies=proxylist,
#     browserUseFastError404Detection=True,
#     useHTTPBrowser=True,
#     crawlingCallback=crawlingCallback,
#     terminatedCallback=terminatedCallback,
#     browserParams=params,
#     logger=Logger(loggerPath)
# )
# crawler.start()


class Spider:
    def __init__\
    (
        self,
        logger=None,
        proxytxtPath=None,
        sitestxtPath=None,
        dbName=None,
        collectionName=None,
        paramsCrawler=None,
        pagesPerSite=None
    ):

        self.logger = logger
        self.proxytxtPath = proxytxtPath
        self.sitestxtPath = sitestxtPath
        self.dbName = dbName
        self.collectionName = collectionName
        self.params = paramsCrawler
        self.pages = pagesPerSite
        sites = [line.rstrip('\n') for line in open(sitestxtPath)]
        proxylist = proxyfromtxt(proxytxtPath, save_dict=True)
        domains = [u.getDomain(site) for site in sites]
        counts = dict((domain, 0) for domain in domains)


    def start(self):
        newscrawlCollection = MongoCollection\
        (
            self.dbName,
            self.collectionName,
            indexOn=["url"],
            indexNotUniqueOn=["lastUrlDomain"],
            # user=user, password=password, host=host,
            version=newsCrawlerVersion,
            giveHostname=True,
            giveTimestamp=True,
            logger=self.logger,
        )

        crawler = Crawler\
        (
            sites,
            proxies=proxylist,
            browserUseFastError404Detection=True,
            useHTTPBrowser=True,
            crawlingCallback=crawlingCallback,
            terminatedCallback=terminatedCallback,
            browserParams=params,
            logger=self.logger
        )

        crawler.start()
