#!/usr/bin/env python
# -*- coding: utf-8 -*-

from robobrowser import RoboBrowser
import getpass

browser = RoboBrowser()
url = 'https://github.com/login'
browser.open(url)

# Get the login form
signin_form = browser.get_form(action='/session')

username = raw_input ("Username: ")
password = getpass.getpass()

# Fill form data
signin_form['login'] = username
signin_form['password'] = password

# Submit form
browser.session.headers['Referer'] = url
signin_form.serialize() 
browser.submit_form(signin_form)

counter = browser.select('span.counter')
print "\nNumber repositories: " + counter[0].text

#obtain links with beautifulSoup
links = browser.select('a.mini-repo-list-item')

for link in links:
	if not link['href'].startswith("https"):
		link['href']='https://github.com'+link['href']
	print "\n"+link['href']
	str = link['href']
	parts = str.split("/")
	user = parts[3]
	title = parts[4]
	#print link
	browser.follow_link(link)
	description = browser.select('div.repository-description')
	if len(description)>0:
		print "Description: " + description[0].text.encode("utf-8").strip()
	
	authors = browser.select('img.avatar')
	
	for author in authors:
		print "Author: "+ author['alt'].encode("utf-8").strip()
		
	enlaces = browser.find_all('a')
	
	for enlace in enlaces:
		if enlace.get('href') == '/'+user+"/"+title+'/commits/master':
			print 'commits '+ enlace.select('span.num')[0].text.strip()
		if enlace.get('href') == '/'+user+"/"+title+'/branches':
			print 'branches '+ enlace.select('span.num')[0].text.strip()
		if enlace.get('href') == '/'+user+"/"+title+'/releases':
			print 'releases '+ enlace.select('span.num')[0].text.strip()
		if enlace.get('href') == '/'+user+"/"+title+'/graphs/contributors':
			print 'contributors '+ enlace.select('span.num')[0].text.strip()
	# Back to results page
	browser.back()