
# pew in 404detector-venv python /home/hayj/wm-dist-tmp/404Detector/error404detector/dataset-maker/makedataset2.py


# rsync -avhu -e "ssh -p 2222" hayj@212.129.44.40:/home/hayj/Data/Misc/error404/ /home/hayj/Data/Misc/error404/



from datatools.url import *
from systemtools.basics import *
from systemtools.duration import *
from systemtools.file import *
from systemtools.logger import *
from systemtools.location import *
from systemtools.hayj import *
from systemtools.system import *
import sh
import random
import re
from queue import *
from databasetools.mongo import *
from newstools.newsurlfilter import *



list404 = \
[
    "https://viralbot360.wordpress.com/2017/01/30/here-are-some-of-the-most-powerful-images-from-airport-protests-across-the-us",
    "http://www.globalresearch.ca/martin-luther-kings-death-disappears-down-the-memory-hole-he-was-assassinated-by-a-u-s-government-conspiracy/5568783?utm_source=dlvr.it&utm_medium=twitter",
    "http://www.nextgov.com/cio-briefing/2017/01/email-privacy-bill-reintroduced-Congress/134475/",
    "https://naijadailyfeed.wordpress.com/2017/01/11/why-i-met-with-buhari-after-ndumes-removal-as-senate-leader-saraki",
    "http://www.usnews.com/news/us/articles/2017-01-01/phillys-mummers-parade-offers-new-year-a-lively-welcome",
    "http://hosted.ap.org/dynamic/stories/S/SOC_WASHINGTON_UNIVERSITY_TEAM_SUSPENDED?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT&CTIME=2016-12-17-12-37-13",
    "http://www.usnews.com/news/politics/articles/2017-01-02/house-gop-votes-to-gut-independent-ethics-office?src=usn_tw",
    "https://bestofticket.wordpress.com/2016/12/15/lastminute-2-x-adult-gold-class-movie-tickets-vouchers-expires-aug-2017-rrp-80-00-australia-61",
    "https://5xforex.wordpress.com/2016/10/07/alert-order-sell-gbpusd-closed-pips-118-7-forex-forexsignals-hyip-forexsignal-makemoneyonline-see-full",
    "http://money.usnews.com/investing/articles/2017-01-25/heres-what-people-are-saying-about-dow-20000?utm_source=dlvr.it&utm_medium=twitter", # acces denied like others...
    "http://customwire.ap.org/dynamic/stories/C/CA_POLICE_TRAFFIC_STOP_SEARCHES_CAOL-?SITE=CASON&SECTION=STATE&TEMPLATE=DEFAULT&CTIME=2016-12-05-19-46-25",
    "http://www.breitbart.com/london/2016/12/14/young-woman-raped-migrant-popular-hamburg-bar/",
    "https://viralbot360.wordpress.com/2016/12/14/top-100-viral-videos-of-the-year-2016-jukinvideo-part-3",
    "http://www.bbc.co.uk/music/artists/7684f1ee-2154-475f-b05d-608c91a0e3e9",
    "http://www.usnews.com/news/national-news/articles/2017-01-24/inauguration-mass-arrest-of-protesters-journalists-a-throwback-with-a-familiar-face-attorneys-say",
    "https://naijadailyfeed.wordpress.com/2016/12/12/prem-36-goals-in-90-seconds-3",
    "https://indbreaking.wordpress.com/2016/12/06/after-supporting-demonetization-nitish-kumar-says-cashless-economy-wont-work-in-india-daily-news-analysis",
    "http://www.thefrisky.com/2016-11-16/uber-driver-allegedly-rapes-drunk-teenage-girl-as-sexual-assault-allegations-involving-drivers-stack-up/",
]

listCaptchaOrSubscribe = \
[
    "http://on.ft.com/2kKIBtV", # Subscribe to read
    "http://www.aei.org/publication/trump-right-chicago-more-dangerous-than-afghanistan-yes-and-no/?utm_source=twitter&utm_medium=social&utm_campaign=thiessenchicagoafg", # Please complete the security check to access
    "http://on.ft.com/2gI1uLB",
    "http://www.ft.com/cms/s/0/d0df9364-d9db-11e6-944b-e7eb37a6aa8e.html?ftcamp=published_links/rss/home_asia/feed//product&utm_source=dlvr.it&utm_medium=twitter",
]


# Init:
(user, password, host) = getMongoAuth(user="hayj", hostname="datascience01")
collection = MongoCollection \
(
    "crawling",
    "taonews",
    user=user,
    password=password,
    host=host,
    indexNotUniqueOn=["last_url_domain", "normalized_url_domain", "status", "crawler"],
    indexOn=["normalized_url"],
)



if True:
    folder = "/home/hayj/Data/Misc/error404/denied/404"
    theList = list404
#     folder = "/home/hayj/Data/Misc/error404/captcha-subscribe/404"
#     theList = listCaptchaOrSubscribe
    for current in theList:
        found = collection.findOne({"normalized_url": current})
        if found is None:
            print("NOT FOUND:")
            print(current)
        else:
            strToFile(found["html"], folder + "/" + str(getRandomInt()) + ".html")




if False:
    for current in collection.find():
        if getRandomFloat() > 0.96 and current["status"] == "success":
            print("\n\n\n\n------------------")
            print(current["normalized_url"])
            print(current["title"])
            print()
            print(current["scrap"]["boilerpipe"]["text"])
            result = input("Press")
            if result == "a":
                print("storriiiing")
                fileNameTitle = ""
                if len(current["title"]) > 40:
                    fileNameTitle = strToFilename(current["title"]).lower()
                    if len(fileNameTitle) > 40:
                        fileNameTitle = fileNameTitle[0:38]
                    else:
                        fileNameTitle = ""
                filePath = dataDir() + "/Misc/error404/from-taonews2/ok/" + fileNameTitle + str(getRandomInt()) + ".html"
                print(filePath)
                strToFile(current["html"], filePath)




