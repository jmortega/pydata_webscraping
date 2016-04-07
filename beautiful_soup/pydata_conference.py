#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from bs4 import BeautifulSoup
import string
import requests
import cookielib
import csv
import json
import codecs

talks_pydata = []

def main():
    url = "http://pydata.org/madrid2016/schedule/"

    data = requests.get(url)

    bs = BeautifulSoup(data.text,"lxml")
    
    print "Links"
    print "-------------------" 
    links = bs.find_all('a')
    for link in links:
            print link
            

    slots = bs.find_all('td', {'class': 'slot slot-talk'})
    
    print "Slots"
    print "-------------------"

    for slot in slots:
        speakers = slot.find_all('span', {'class': 'speaker'})
	urls = slot.find_all('span', {'class': 'title'})
	i=0
	for speaker in speakers:
	    name_speaker = speaker.text.strip()
	    elements= urls[i].find_all('a')
	    for element in elements:
		url = element['href']
		talk = element.text
	    i=i+1
	    talk_pydata = {}
	    if name_speaker is not None and url is not None and talk is not None:
		talk_pydata['speaker'] = name_speaker.encode('utf-8')
		talk_pydata['url'] = url.encode('utf-8')
		talk_pydata['talk'] = talk.encode('utf-8')
		talks_pydata.append(talk_pydata)
	
                               
if __name__=="__main__":
    main()
    
    file = codecs.open("pydata_conference.json", "wb", encoding="UTF-8")
    file.write("[")
    
    index = 0
    
    for talk_pydata in talks_pydata:
        print talk_pydata['speaker'].decode('utf-8').encode('cp850','replace').decode('cp850')
        print talk_pydata['url'].decode('utf-8').encode('cp850','replace').decode('cp850')
        print talk_pydata['talk'].decode('utf-8').encode('cp850','replace').decode('cp850')
	line = json.dumps(talk_pydata,indent=4) + "\n"
        index = index + 1	
	if(index<len(talks_pydata)):
	    file.write(line+",")
	else:
	    file.write(line)
		
	print "------------------"
	
    file.write("]")
	
    with open('pydata_conference.csv' ,'wb') as csvfile: 
            pydata_writer = csv.writer(csvfile)
            for result in talks_pydata:
                pydata_writer.writerow([str(result['speaker']),str(result['url']),str(result['talk'])])
	
	
	
