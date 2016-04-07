# imports
import mechanize
from bs4 import BeautifulSoup
# Create a Browser
b = mechanize.Browser()

# Disable loading robots.txt
b.set_handle_robots(False)

b.addheaders = [('User-agent',
                 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98;)')]

# Navigate
b.open('http://www.google.com/')

# Choose a form
b.select_form(nr=0)

# Fill it out
b['q'] = 'pydata'

# Stubmit
fd = b.submit()

response =  fd.read()

# ... process the results
soup = BeautifulSoup(response,"lxml")
for link in soup.find_all('a'):
    print(link.get('href'))

