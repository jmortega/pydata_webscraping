import urllib,urllib2
import urlparse
from bs4 import BeautifulSoup
import os, sys
import requests


def getAllImages(url):
    query = urllib2.Request(url)
    user_agent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 1.0.3705)"
    query.add_header("User-Agent", user_agent)

    #create directory for save images
    os.system("mkdir images")
    
    bs = BeautifulSoup(urllib2.urlopen(query),"lxml")
    for img in bs.findAll("img"):
        print "found image"
        src = img["src"]
        if src:
            src1 = src
            print src1
            r = requests.get(src1,stream=True)
            f = open('images/%s' % src1.split('/')[-1], 'wb')
            f.write(r.content)
            f.close()

getAllImages("http://pydata.org/madrid2016/schedule/")
