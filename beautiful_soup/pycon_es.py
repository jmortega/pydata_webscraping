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

talks_pycones = []

def main():
    url = "http://2015.es.pycon.org/es/schedule/"

    data = requests.get(url)

    bs = BeautifulSoup(data.text,"lxml")
    
    print "Links"
    print "-------------------" 
    links = bs.find_all('a')
    for link in links:
            print link
            
    days = bs.find_all('div', {'class': 'col-xs-12 day'})

    print "Days"
    print "-------------------"
    
    for day in days:
            print day.find("h2").text

    slots = bs.find_all('div', {'class': 'slot'})
    
    print "Slots"
    print "-------------------"

    for slot in slots:
        demo = slot.find_all('div', {'class': 'col-xs-12'})
        for slot in demo:
            if slot is not None:
                slot2 = slot.find_all('div', {'class': 'slot-inner'})
                for aux in slot2:
                    speaker = aux.find('p').find('strong')
                    title = aux.find('h3')
                    hour = aux.find('strong')
                description = slot.find('p')
                talk_pycones = {}
                if speaker is not None and title is not None and hour is not None and description is not None and speaker.text.encode('utf-8') != description.text.encode('utf-8'):
                    talk_pycones['speaker'] = speaker.text.encode('utf-8')
                    talk_pycones['title'] = title.text.encode('utf-8')
                    talk_pycones['hour'] = hour.text.encode('utf-8')
                    talk_pycones['description'] = description.text.encode('utf-8')
                    talks_pycones.append(talk_pycones)
                               
if __name__=="__main__":
    main()
    
    file = codecs.open("pycones.json", "wb", encoding="UTF-8")
    file.write("[")
    
    index = 0
    
    for talk_pycones in talks_pycones:
	print talk_pycones['description'].decode('utf-8').encode('cp850','replace').decode('cp850')
        print talk_pycones['hour'].decode('utf-8').encode('cp850','replace').decode('cp850')
        print talk_pycones['title'].decode('utf-8').encode('cp850','replace').decode('cp850')
        print talk_pycones['speaker'].decode('utf-8').encode('cp850','replace').decode('cp850')
	line = json.dumps(talk_pycones,indent=4) + "\n"
        index = index + 1	
	if(index<len(talks_pycones)):
	    file.write(line+",")
	else:
	    file.write(line)
		
	print "------------------"
	
    file.write("]")
	
    with open('pycones.csv' ,'wb') as csvfile: 
            pycones_writer = csv.writer(csvfile)
            for result in talks_pycones:
                pycones_writer.writerow([str(result['description']),str(result['hour']),str(result['title']),str(result['speaker'])])
	
	
	
