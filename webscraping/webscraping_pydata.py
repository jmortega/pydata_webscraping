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
html = D.get('http://pydata.org/madrid2016/schedule/')

talks_pydata = []

#get td element where is located information
for row in xpath.search(html, '//td[@class="slot slot-talk"]'):
	
	speakers = xpath.search(row,'//span[@class="speaker"]/text()')
	urls = xpath.search(row,'//span[@class="title"]//a/@href')
	talks = xpath.search(row,'//span[@class="title"]//a/text()')	
	for speaker in speakers:
		print speaker.strip()
		print urls[0]
		print talks[0]
		details = D.get('http://pydata.org/'+urls[0])
		description = xpath.search(details,'//div[@class="description"]//p/text()')[0]
		print description
		hour = xpath.search(details,'//div[@class="col-md-8"]//h4/text()')[0].replace("\n","").strip()
		print hour
		
		if talks[0] is not None and speaker is not None and description is not None and hour is not None:
			talk_pydata ={}
			talk_pydata['talk'] = talks[0].decode('utf-8').encode('cp850','replace').decode('cp850')
			talk_pydata['speaker'] = speaker.strip().decode('utf-8').encode('cp850','replace').decode('cp850')
			talk_pydata['description'] = description.decode('utf-8').encode('cp850','replace').decode('cp850')
			talk_pydata['url'] = urls[0].decode('utf-8').encode('cp850','replace').decode('cp850')
			talk_pydata['hour'] = hour.decode('utf-8').encode('cp850','replace').decode('cp850')
			    
			talks_pydata.append(talk_pydata)		
		
		print "---------------------\n"  
	
        
file = codecs.open("pydata.json", "wb", encoding="UTF-8")

file.write("[")
index=0

for talk_pydata in talks_pydata:
	
        print talk_pydata['talk']
        print talk_pydata['speaker']
        print talk_pydata['description']
	print talk_pydata['url']
        print talk_pydata['hour']
        line = json.dumps(talk_pydata,indent=4) + "\n"

	index = index + 1	
	if(index<len(talks_pydata)):
		file.write(line+",")
	else:
		file.write(line)
	

	print "------------------"
	
file.write("]")

with codecs.open('pydata.csv' ,'wb') as csvfile:
	pydata_writer = csv.writer(csvfile)
	for result in talks_pydata:
		pydata_writer.writerow([str(result['talk'].encode('utf-8')),
		                        str(result['speaker'].encode('utf-8')),
		                        str(result['description'].encode('utf-8')),
		                        str(result['url'].encode('utf-8')),
		                        str(result['hour'].encode('utf-8'))])
    
