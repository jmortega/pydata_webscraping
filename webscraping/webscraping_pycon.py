#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webscraping import download, xpath
import json
import csv
import sys
import codecs


#Download instance
D = download.Download()

#get page
html = D.get('http://2015.es.pycon.org/es/schedule/')

index =0
talks_pycones = []

#get div where is located information
for row in xpath.search(html, '//div[@class="col-xs-12"]'):
    
    if index%2 ==0:
        talk = xpath.search(row, '//div[@class="slot-inner"]/h3')
    
        author = xpath.search(row, '//div[@class="slot-inner"]/p/strong')
    
        hour = xpath.search(row, '//div[@class="slot-inner"]/strong')
        
    if index%2 !=0:
        description = xpath.search(row, '/p')
        
        if talk is not None and author is not None and description is not None and hour is not None and len(talk)>0 and len(author)>0 and len(description)>0 and len(hour)>0:
            talk_pycones ={}
            talk_pycones['talk'] = talk[0].decode('utf-8').encode('cp850','replace').decode('cp850')
            talk_pycones['author'] = author[0].decode('utf-8').encode('cp850','replace').decode('cp850')
            talk_pycones['description'] = description[0].decode('utf-8').encode('cp850','replace').decode('cp850')
            talk_pycones['hour'] = hour[0].decode('utf-8').encode('cp850','replace').decode('cp850')
            
            talks_pycones.append(talk_pycones)

    index+=1


with open('pycones.json','w') as outfile:
    json.dump(talks_pycones,outfile,indent=4)

with codecs.open('pycones.csv' ,'wb') as csvfile:
	pycones_writer = csv.writer(csvfile)
	for result in talks_pycones:
            pycones_writer.writerow([str(result['talk'].encode('utf-8')),
	                             str(result['author'].encode('utf-8')),
	                             str(result['description'].encode('utf-8')),
	                             str(result['hour'].encode('utf-8'))])
    
