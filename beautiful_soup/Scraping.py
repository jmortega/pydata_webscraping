# -*- encoding: utf-8 -*-
#class for scraping

import os

import requests
from lxml import html

from bs4 import BeautifulSoup
import urlparse

class Scraping:
    
    def scrapingBeautifulSoup(self,url):
    
        try:
            print("BeautifulSoup..............")
            
            response = requests.get(url)
            print response
            bs = BeautifulSoup(response.text, 'lxml')
            for tagImage in bs.find_all("img"): 
                #print(tagImage['src'])
                if tagImage['src'].startswith("http") == False:
                    download = url + tagImage['src']
                else:
                    download = tagImage['src']
                print download
                # download images in img directory
                r = requests.get(download)
                f = open('images/%s' % download.split('/')[-1], 'wb')
                f.write(r.content)
                f.close()
        
        except Exception,e:
                print e
                print "Error to connect with " + url + " for scraping the site" 
                pass
				
    def scrapingImagesPdf(self,url):
        print("\nScraping the server for images and pdfs.... "+ url)
    
        try:
            response = requests.get(url)  
            parsed_body = html.fromstring(response.text)

            # Grab links to all images
            images = parsed_body.xpath('//img/@src')

            print 'Found %s images' % len(images)
    
            #create directory for save images
            os.system("mkdir images")
    
            for image in images:
                if image.startswith("http") == False:
                    download = url + image
                else:
                    download = image
                print download
                # download images in images directory
                r = requests.get(download)
                f = open('images/%s' % download.split('/')[-1], 'wb')
                f.write(r.content)
                f.close()
    

            # Grab links to all pdf
            pdfs = parsed_body.xpath('//a[@href[contains(., ".pdf")]]/@href')
    
            #create directory for save pdfs
            if len(pdfs) >0:
                os.system("mkdir pdfs")
        
            print 'Found %s pdf' % len(pdfs)
            for pdf in pdfs:
                if pdf.startswith("http") == False:
                    download = url + pdf
                else:
                    download = pdf
                print download
                # download pdfs in pdf directory
                r = requests.get(download)
                f = open('pdfs/%s' % download.split('/')[-1], 'wb')
                f.write(r.content)
                f.close()
    
        except Exception,e:
                print e
                print "Error to connect with " + url + " for scraping the site" 
                pass
