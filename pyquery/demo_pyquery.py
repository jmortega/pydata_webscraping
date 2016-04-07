#!/usr/bin/env python

#import pyquery
from pyquery import *
import json
import csv
import sys
import codecs

#its create an instance of the PyQuery class
html = PyQuery(url='http://2015.es.pycon.org/es/schedule/')

index =0
talks_pycones = []

#obtain div where can be found each conference info
for row in html('div.col-xs-12'):
    if index%2 ==0:
        PyQueryTalk = PyQuery(row)
        talk = PyQueryTalk('div.slot-inner h3').text().encode('utf-8')
        author = PyQueryTalk('p').text().encode('utf-8')
        hour = PyQueryTalk('strong').text().encode('utf-8')   

    if index%2 !=0:
        
        description = PyQuery(row)
        description2 = description('p').text().encode('utf-8')  
        if talk is not None and author is not None and description is not None and hour is not None and len(talk)>0 and len(author)>0 and len(description)>0 and len(hour)>0:
            talk_pycones ={}
            talk_pycones['talk'] = talk
            talk_pycones['author'] = author
            talk_pycones['description'] = description2
            talk_pycones['hour'] = hour
            talks_pycones.append(talk_pycones)
        
    index+=1


with open('pycones.json','w') as outfile:
    json.dump(talks_pycones,outfile,indent=4)