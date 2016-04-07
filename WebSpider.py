import multiprocessing
import sys
from bs4 import BeautifulSoup
import mechanize
import argparse
import urllib
import urllib2
import time
import sqlite3

class WebSpider():

	def __init__(self, webSite, depth, proxyhost, proxyuser, proxypassword, proxyport,proxysecure="http"):
		try:
			self.webSite = webSite
			self.depth = int(depth)
			self.totalDeepCrawled = 0
			self.linksVisited = [self.webSite]
			self.totalProfundity = 0;
			self.proxyhost = proxyhost
			self.proxyuser = proxyuser
			self.proxypassword = proxypassword
			self.proxysecure = proxysecure
			self.proxyport = proxyport
			self.proxies = None
			if self.proxyhost != None and self.proxyport != None:
				if self.proxyuser != None and self.proxypassword != None: 
					self.proxies = urllib2.ProxyHandler({self.proxysecure: self.proxysecure+"://"+self.proxyuser+":"+self.proxypassword+"@"+self.proxyhost+":"+self.proxyport})
				else:
					print self.proxysecure
					print self.proxyhost
					print self.proxyport
					self.proxies = urllib2.ProxyHandler({self.proxysecure: self.proxysecure+"://"+self.proxyhost+":"+self.proxyport})
					self.proxies = {self.proxysecure: self.proxysecure+"://"+self.proxyhost+":"+self.proxyport}
			#Perform the connection with the database.
			print "[*] Performing Connection with Database..."

			self.db = sqlite3.connect('db.sqlite3')
			self.db.execute("create table if not exists WebSites(webSiteRoot VARCHAR(100), contents VARCHAR(1000000), id integer primary key autoincrement);")
			self.db.execute("create table if not exists WebSiteLinks(id integer primary key autoincrement, idWebSiteRoot integer NOT NULL, link VARCHAR(500));")
			self.db.execute("create table if not exists WebSiteForms(id integer primary key autoincrement, idWebSiteRoot integer NOT NULL, formAction VARCHAR(500), formName VARCHAR(500), formMethod VARCHAR(20));")
			
			self.db.execute("create table if not exists FormData(id integer primary key autoincrement, idWebSiteForm integer, attributeName VARCHAR(200), attributeValue VARCHAR(200), attributeType integer);")
			
			#create table WebSites(webSiteRoot VARCHAR(100) NOT NULL, contents VARCHAR(1000000) NOT NULL, id MEDIUMINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id))
			
			#CREATE TABLE WebSiteLinks(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteRoot MEDIUMINT NOT NULL, link VARCHAR(500) NOT NULL, PRIMARY KEY (id));
			
			#CREATE TABLE WebSiteForms(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteRoot MEDIUMINT NOT NULL, formAction VARCHAR(500), formName VARCHAR(500), formMethod #VARCHAR(20), PRIMARY KEY (id));
			
			#CREATE TABLE FormData(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteForm MEDIUMINT NOT NULL, attributeName VARCHAR(200), attributeValue VARCHAR(200), attributeType #MEDIUMINT, PRIMARY KEY(id) )			

			self.cursorDB = self.db.cursor()
			print "Database db.sqlite3 created succesfully"		

			print "[*] Connection Established!" 
		except Exception,e:
			print str(e)
			print "[-] Exception trying to connect with the database. Check the connection settings for the MySQL instance"
			print "[-] We can't continue... closing the program."
			print sys.exc_info()[0]
			print sys.exc_info()[1]
			print sys.exc_info()[2]
			sys.exit(0)

	def crawl(self):
		print "[*] Starting the web crawling ..."
		if self.proxies != None:
			print "Using HTTP proxy %s" % self.proxies['http']			
			urlRootSite = urllib.urlopen(self.webSite,proxies=self.proxies)
		else:
			urlRootSite = urllib.urlopen(self.webSite)
		contents = urlRootSite.read()
		rootSite = BeautifulSoup(contents,"lxml")
		links = rootSite.find_all("a")
		print links
		print "[*] Getting the links for the URL: ", self.webSite
		self.idWebSiteRoot = self.storeWebSiteRoot(self.webSite.decode('utf-8'), contents.decode('utf-8'))
		self.storeWebSiteForms(self.webSite.decode('utf-8'))
		self.storeWebSiteLinks(links)
		try:
			for link in links:
				#process = multiprocessing.Process(target=self.handleLink, args=[link])
				#process.daemon = True
				#process.start()	
				#process.join()
				self.handleLink(link)				
				self.totalProfundity = 0
		finally:
			self.db.close()
			self.cursorDB.close()
		
	def handleLink(self, link):
		self.totalProfundity = self.totalProfundity + 1	
		if ('href' in dict(link.attrs) and "http" in link['href']):
			try:
				href = link["href"]
				if href in self.linksVisited:
					return
				if self.proxies != None:
					urlLink = urllib.urlopen(href,proxies=self.proxies)
				else:
					urlLink = urllib.urlopen(href)
				self.linksVisited.append(link['href'])
				print "Handling Link %s. url: %s" %(link.text, link['href'])
				#Extract info about the link, before to get links in this page.
				if self.totalProfundity <= self.depth:
					linkSite = BeautifulSoup(urlLink, "lxml")
					depthLinks = linkSite.find_all("a")				
					self.storeWebSiteForms(link['href'])
				        self.storeWebSiteLinks(depthLinks)
					for sublink in depthLinks:
						#processLink = multiprocessing.Process(target=self.handleLink, args=[sublink])
	        	        		#processLink.daemon = True
						#processLink.start()
						self.handleLink(sublink)
				else:
					self.totalProfundity = self.totalProfundity - 1
					return
			except:
				print "[-] Error in Link..."	
				print link
				print sys.exc_info()[1]
	'''
		SQL Table: 
		create table WebSites(webSiteRoot VARCHAR(100) NOT NULL, contents VARCHAR(1000000) NOT NULL, id MEDIUMINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id));
	'''
	def storeWebSiteRoot(self,url, contents):
		try:
			#insertSQL = "INSERT INTO WebSiteRoot (webSiteRoot,contents) values (%s, %s)", (str(url), str(contents))
			#self.cursorDB.execute("""INSERT INTO WebSites (webSiteRoot,contents) values (%s, %s)""", (url, contents))
			insert = "insert into WebSites(webSiteRoot, contents) values(?,?)"
			self.cursorDB.execute(insert, (url, contents))
			self.db.commit()
			#obtain last id inserted in DB WebSites
			return self.cursorDB.lastrowid
		except Exception,e:
			print "[-] Exception trying to insert the WebSite root in database."
			print str(e)
			self.db.rollback()

	'''
		SQL Table:
		CREATE TABLE WebSiteLinks(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteRoot MEDIUMINT NOT NULL, link VARCHAR(500) NOT NULL, PRIMARY KEY (id));
	'''
	def storeWebSiteLinks(self, links):
		try:
			for link in links:
				if ('href' in dict(link.attrs) and "http" in link['href']):
					insert = "insert into WebSiteLinks(idWebSiteRoot, link) values(?,?)"
					self.cursorDB.execute(insert, (str(self.idWebSiteRoot), link['href']))
					
					#self.cursorDB.execute("INSERT INTO WebSiteLinks (idWebSiteRoot,link) values (%s, %s)", (str(self.idWebSiteRoot), link['href']))
	                        	self.db.commit()
		except:
			self.db.rollback()
			print "Exception trying to insert a web link."

	'''
		SQL Table:
		CREATE TABLE WebSiteForms(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteRoot MEDIUMINT NOT NULL, formAction VARCHAR(500), formName VARCHAR(500), formMethod VARCHAR(20), PRIMARY KEY (id));
		CREATE TABLE FormData(id MEDIUMINT NOT NULL AUTO_INCREMENT, idWebSiteForm MEDIUMINT NOT NULL, attributeName VARCHAR(200), attributeValue VARCHAR(200), attributeType MEDIUMINT, PRIMARY KEY(id) )
	'''		
	def storeWebSiteForms(self, url):
		browser = mechanize.Browser()		
		if self.proxies != None:
			browser.set_proxies(self.proxies)
		browser.open(url)
		try:
			for form in browser.forms():
				insert = "insert into WebSiteForms(idWebSiteRoot, formAction,formName,formMethod) values(?,?,?,?)"
				
				self.cursorDB.execute(insert, (str(self.idWebSiteRoot), form.action.decode('utf-8'),form.name.decode('utf-8'),form.method.decode('utf-8')))
				
				#self.cursorDB.execute("INSERT INTO WebSiteForms (idWebSiteRoot,formAction, formName, formMethod) values (%s, %s, %s, %s)", (str(self.idWebSiteRoot), #form.action,form.name,form.method))
				
				self.db.commit()
				#self.cursorDB.execute("SELECT Auto_increment FROM information_schema.tables WHERE table_name='WebSiteForms';")
	                        idForm = self.cursorDB.lastrowid
				for control in form.controls:
					controlName = control.name
					controlType = control.type
					controlValue = control.value
					if controlName == None:
						controlName = ""
					if controlType == None:
						controlType = ""
					if controlValue == None:
						controlValue = ""
					#print str(controlName) +" - "+str(controlType)+" - "+ str(controlValue)
					insert2 = "insert into FormData(idWebSiteForm, attributeName,attributeValue,attributeType) values(?,?,?,?)"
					self.cursorDB.execute(insert2, (str(idForm), str(controlName), str(controlValue), str(controlType)))
					
	        	                #self.cursorDB.execute("INSERT INTO FormData (idWebSiteForm,attributeName,attributeValue,attributeType) values (%s, %s, %s, %s)", (str(idForm), #str(controlName), str(controlValue), str(controlType)))
					self.db.commit()
		except AttributeError:
			pass
		except Exception,e:
			self.db.rollback()
			print "Exception trying to insert a web form. Storing error..."
			print str(e)


if __name__ == "__main__":
	#python WebSpider.py -t url -d 1 -l proxy_host -m proxy_port -s http
	
	parser = argparse.ArgumentParser(description="Python WebSpider")
	parser.add_argument("-t", "--target", required=True,  help="Target website")
	parser.add_argument("-d", "--depth", required=False, help="Number of links to crawl")

	parser.add_argument("-l", "--host", required=False, help="Proxy Host")
	parser.add_argument("-u", "--user", required=False, help="Proxy user")
	parser.add_argument("-p", "--password", required=False, help="Proxy password")
	parser.add_argument("-s", "--secure", required=False, help="Proxy protocol (HTTP/HTTPS)")
	parser.add_argument("-m", "--port", required=False, help="Proxy port")	
	
	
	try:
		args = parser.parse_args()

		spider = WebSpider(args.target,args.depth,args.host,args.user,args.password,args.port,args.secure)
		spider.crawl()
	except KeyboardInterrupt:
		sys.exit(0)
	except SystemExit:
		pass
	except Exception,e:
		print "[-] Fatal Error captured..."
		print str(e)
		print sys.exc_info()[0]
		print sys.exc_info()[1]
		print sys.exc_info()[2]
