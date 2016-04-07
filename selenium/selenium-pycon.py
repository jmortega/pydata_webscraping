from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import csv
import json

url1="http://2015.es.pycon.org/es/schedule/"

urls=[url1]

talks_pycones = []

for url in urls:
    print "url:  "+ url
    browser = webdriver.Firefox()
    browser.get(url)

    days= browser.find_elements_by_xpath("//h2")

    index = 0
    for index in range(0,100):
        try:
            talks= browser.find_elements_by_xpath("//div["+str(index)+"]/div/div/div/div/h3")
            authors= browser.find_elements_by_xpath("//div["+str(index)+"]/div/div/div/div/p/strong")
            hours = browser.find_elements_by_xpath("//div["+str(index)+"]/div/div/div/div/strong")
        except Exception:
                pass

	index_talk = 0
	if len(talks)>0:
            for talk in talks:
                talk_pycones = {}
                if index<=7:
                    talk_pycones['day'] = days[0].text.encode('utf-8')
                if index>=7 and index<=24:
                    talk_pycones['day'] = days[1].text.encode('utf-8')
                if index>=24:
                    talk_pycones['day'] = days[2].text.encode('utf-8')
                talk_pycones['title'] = talk.text.encode('utf-8')
                talk_pycones['speaker'] = authors[index_talk].text.encode('utf-8')
                talk_pycones['hour'] = hours[index_talk].text.encode('utf-8')
                index_talk +=1
                index +=1
                talks_pycones.append(talk_pycones)
								
browser.close()


for talk_pycones in talks_pycones:

        print talk_pycones['day'].encode('utf-8')
        print talk_pycones['hour'].encode('utf-8')
        print talk_pycones['title']
        print talk_pycones['speaker']

	print "------------------"

with open('pycones.csv' ,'wb') as csvfile: 
	pycones_writer = csv.writer(csvfile)
	for result in talks_pycones:
            pycones_writer.writerow([str(result['day']),str(result['hour']),str(result['title']),str(result['speaker'])])
			
with open('pycones.json','w') as outfile:
	json.dump(talks_pycones,outfile)
	

