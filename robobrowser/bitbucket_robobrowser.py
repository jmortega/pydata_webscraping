from robobrowser import RoboBrowser
import getpass


browser = RoboBrowser()
url = 'https://bitbucket.org/account/signin/'
browser.open(url)

# Get the login form
signin_form = browser.get_form(id='aid-login-form')

username = raw_input ("Username: ")
password = getpass.getpass()

# Fill form data
signin_form['username'] = username
signin_form['password'] = password

# Submit form
browser.session.headers['Referer'] = url
signin_form.serialize() 
browser.submit_form(signin_form)

url = 'https://bitbucket.org/dashboard/pullrequests?section=teams'
browser.open(url)
links = browser.select('tr.iterable-item')
for link in links:
	print "Repository: " + link.select('td.repo')[0].text.encode("utf-8").strip()
	print "User: " + link.select('td.user')[0].text.encode("utf-8").strip()
	print "Title: " + link.select('td.title')[0].select('a.execute')[0].text.encode("utf-8").strip()
	print "Updated " + link.select('td.date')[0].text.encode("utf-8").strip()
	print "\n----------------------"
#obtain links with beautifulSoup
links = browser.find_all('a')
for link in links:
	try:
		#print(link.get('href'))
		#if not link['href'].startswith("https"):
			#link['href']='https://bitbucket.org'+link['href'].encode("utf-8").strip()
			#link['href']='/odigeoteam/frontend-html5'
		print link['href']
		#print link
		browser.follow_link(link)
	
		branches = browser.select('li.branches')
		if len(branches)>0 :
			print 'branches '+ branches[0].select('span.value')[0].text
	
		tags = browser.select('li.tags')
		if len(tags)>0 :
			print 'tags' + tags[0].select('span.value')[0].text
	
		enlaces = browser.find_all('a')
		#print enlaces
		for enlace in enlaces:
			if enlace.get('href') == '#forks':
				print 'forks '+ enlace.select('span.value')[0].text
			if enlace.get('href') == '#tags':
				print 'tags '+ enlace.select('span.value')[0].text
			if enlace.get('href') == '#branches':
				print 'branches '+ enlace.select('span.value')[0].text
			if enlace.get('href') == '#followers':
				print 'watchers '+ enlace.select('span.value')[0].text
			# Back to results page
			browser.back()
	except Exception:
		pass

