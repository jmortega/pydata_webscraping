from bs4 import BeautifulSoup
import datetime
import random
import re
import requests
import json

random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = requests.get("http://en.wikipedia.org"+articleUrl).text
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
    #Format of revision history pages is: 
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("history url is: "+historyUrl)
    html = requests.get(historyUrl).text
    bsObj = BeautifulSoup(html)
    #finds only the links with class "mw-anonuserlink" which has IP addresses 
    #instead of usernames
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList


def getCountry(ipAddress):
    try:
        response = requests.get("http://ip-api.com/json/"+ipAddress).text
        responseJson = json.loads(response)
        return responseJson.get("country")        
    except Exception,e:
        print e
    
    
links = getLinks("/wiki/Python_(programming_language)")

print len(links)

while(len(links) > 0):
    for link in links:
        print("-------------------") 
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            if country is not None:
                print(historyIP+" is from "+country)