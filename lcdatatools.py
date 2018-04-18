# -*- coding: utf-8 -*-
# @Author: lichenle
# @Date:   2018-04-08 09:53:02
# @Last modified by:   lichenle
# @Last modified time: 2018-4-18 23:20:20

import sys
import os
import threading
from pymongo import MongoClient
from webcrawler.crawler import *
from databasetools.mongo import *
from lcdatatools import proxyfromtxt
from bs4 import BeautifulSoup


def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()


def proxyfromtxt(
                fileorlist,
                save_dict=False,
                list_keys=None,
                local_test=False
                ):
    f = open(fileorlist, 'r')
    lines = f.readlines()
    list_keys = ['ip', 'port', 'user', 'password']
    list_dict = []
    for line in lines:
        parts = line.strip('\n').split(':')
        list_dict.append(dict(zip(list_keys, parts)))
    if save_dict:
        f_out = open('/Users/lichenle/Desktop/Proxies.txt', 'w')
        deleteContent(f_out)
        print(*list_dict, sep='\n', file=f_out)
        # print(list_dict)
        # print('\n'.join(map(str, list_dict)))
    print('proxy done')
    return list_dict


# def urlJoin(url, site):
#     return site+url if '/' == url[0] else url

def getUrl(html, url):
    global u
    if u is None:
        u = URLParser()
#     print('Getting Urls')
    soup = BeautifulSoup(html, "html.parser")
#     print("Soup Ready")
    urls = []
    try:
        for link in soup.find_all("a"):
            # print('Links')
            href = link.get('href')
            href = u.join(url, href)
            urls.append(href)
            # if checkDomain(href, url):
            #     urls.append(href)
    except Exception as e:
        print(str(e)+'getUrl')
    return urls


def main():
    list_dict = proxyfromtxt(sys.argv[1], save_dict=sys.argv[2])
    # print(list_dict)


if __name__ == "__main__":
    main()
    # list_dict = lisfiletTodict('/Users/lichenle\
    # /Desktop/Untitled Folder/proxies.txt', save_dict='True')
