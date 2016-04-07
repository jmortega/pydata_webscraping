from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import csv
import json
import time

url1="http://2015.codemotion.es/agenda.html#5677904553836544"
url2="http://2015.codemotion.es/agenda.html#5699289732874240"

urls=[url1,url2]

i=0

talks_codemotion = []
talks_codemotion_details = []

for url in urls:
    print "url:  "+ url
    browser = webdriver.Firefox()
    browser.get(url)

    days= browser.find_elements_by_xpath("//section[2]/div/div/ul/li/a")
    if days is not None and len(days)>0:
        print days[i].text
        
    links = browser.find_elements_by_class_name("ka-talk-title")


    for link in links:
        try:
            print link.get_attribute('href')
            link.click()
            talk_codemotion={}
            aux = browser.find_element_by_class_name("ka-talk-details-title")
            author = browser.find_element_by_class_name("ka-author-name")
            description = browser.find_element_by_class_name("ka-talk-details-description")
            tags = browser.find_elements_by_class_name("tag")
            tags_aux=""

            if tags is not None and len(tags)>0:
                for tag in tags:
                   tags_aux = tags_aux + "-" + tag.text.encode('utf-8')
            talk_codemotion['tags'] = tags_aux

            if aux is not None:
                talk_codemotion['title'] = aux.text.encode('utf-8')

            if author is not None:    
                talk_codemotion['speaker'] = author.text.encode('utf-8')

            if description is not None:
                talk_codemotion['description'] = description.text.encode('utf-8')
            
            
            talks_codemotion_details.append(talk_codemotion)
            
            time.sleep(3)
            
        except Exception,e:
            pass

    for index in range(0,20):

        for columna in range(2,15):
            try:
                hour= browser.find_element_by_xpath("//tr["+str(index)+"]/td")
                talks= browser.find_elements_by_xpath("//tr["+str(index)+"]/td["+str(columna)+"]/p")
                talk_codemotion = {}
                talk_codemotion['day'] = ""
                index_aux = 0
                if len(talks)>0:
                    for talk in talks:  
                        if days is not None and len(days)>0:
                            talk_codemotion['day'] = days[i].text
                        elif i==0:
                            talk_codemotion['day'] = "27 Noviembre"
                        elif i==1:
                            talk_codemotion['day'] = "28 Noviembre"
                        if hour is not None:
                            talk_codemotion['hour'] = hour.text
                        if index_aux ==0 and talk is not None:
                            talk_codemotion['title'] = talk.text.encode('utf-8')
                        if index_aux ==1 and talk is not None:   
                            talk_codemotion['speaker'] = talk.text.encode('utf-8')
                        index_aux +=1
                    talks_codemotion.append(talk_codemotion)
            except Exception:
                pass
    i=i+1
	
browser.close()

file = open('codemotion.json' ,'wb')
file_details = open('codemotion_details.json' ,'wb')


for talk_codemotion in talks_codemotion:

        print talk_codemotion['day'].encode('utf-8')
        print talk_codemotion['title']
        print talk_codemotion['speaker']
        print talk_codemotion['hour']
        line = json.dumps(talk_codemotion) + "\n"
        file.write(line)

	print "------------------"
	

for talk_codemotion in talks_codemotion_details:

        print talk_codemotion['title']
        print talk_codemotion['speaker']
        print talk_codemotion['description']
        print talk_codemotion['tags']
        line_details = json.dumps(talk_codemotion) + "\n"
        file_details.write(line_details)

	print "------------------"

with open('codemotion_details.csv' ,'wb') as csvfile: 
	codemotion_details_writer = csv.writer(csvfile)
	for result in talks_codemotion_details:
            codemotion_details_writer.writerow([str(result['title']),str(result['speaker']),str(result['description']),str(result['tags'])])
			

with open('codemotion.csv' ,'wb') as csvfile: 
	codemotion_writer = csv.writer(csvfile)
	for result in talks_codemotion:
            codemotion_writer.writerow([str(result['day'].encode('utf-8')),str(result['title']),str(result['speaker']),str(result['hour'])])

