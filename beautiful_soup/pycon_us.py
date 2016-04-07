import csv
import json
import requests
import requests
from bs4 import BeautifulSoup

SCHED_PAGE='https://us.pycon.org/2013/schedule/'

data = requests.get(SCHED_PAGE)
soup = BeautifulSoup(data.text,"lxml")


results = []

for table_row in soup.select(".slot"):

	details = {}
	boolhref=False
	booltitle=False
	boolspeaker=False
	
	if table_row.find('a') is not None:
		boolhref = True
		href = table_row.find('a')['href']
		details['href'] = href
	if table_row.find('a') is not None:
		booltitle = True
		title = table_row.find('a')
		details['title'] = title.text.encode('utf-8')
	if table_row.find('span',attrs={"class": "speaker"}) is not None:
		boolspeaker=True
		speaker = table_row.find('span',attrs={"class": "speaker"})
		details['speaker'] = speaker.text.encode('utf-8').strip()
	
	if boolhref and booltitle and boolspeaker:
		results.append(details)

print len(results)

# We now have details (in our dictionary) for each inmate. Let's print those out.
for result in results:
	print '{0}'.format(result['href'])
	print '{0}'.format(result['title'])
	print '{0}'.format(result['speaker'])
	print ''
	
with open('pycon_us.csv' ,'wb') as csvfile: 
	pyconwriter = csv.writer(csvfile)
	for result in results:
			pyconwriter.writerow([str(result['title'].encode('utf-8')),str(result['speaker'])])
			
with open('pycon_us.json','w') as outfile:
	json.dump(results,outfile,indent=4)	