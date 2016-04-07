import sys
import string
import requests
from bs4 import BeautifulSoup
import io

f = io.open('imdb.txt', 'w', encoding='utf8')
print "Generating new file (imdb.txt)."
try:
		r  = requests.get('http://www.imdb.com/chart/top')
		
		data = r.text

		soup = BeautifulSoup(data,"lxml")

		f = open("imdb.txt", "w")
		
		table = soup.find('table')
		
		links = table.findAll('a')
		for item in links:
			if item.string is not None:
				print item.string
				f.write(item.string.encode('utf8')  + '\n')
		f.close()
except Exception,e:
		print "Target file (imdb250.htm) could not be found."
		print e