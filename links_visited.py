import urlparse
import urllib
from bs4 import BeautifulSoup
import requests

url = "http://pydata.org/madrid2016/"

urls = [url]
visited= [url]

while len(urls)>0:
        try:
                htmltext = requests.get(url).text;
        except:
                print urls[0]
        soup = BeautifulSoup(htmltext,"lxml")
        
        print urls.pop(0)
        
        
        for tag in soup.findAll('a',href=True):
                tag['href'] = urlparse.urljoin(url,tag['href'])
                if url in tag['href'] and tag['href'] not in visited:
                        urls.append(tag['href'])
                        visited.append(tag['href'])
        
print urls
print visited