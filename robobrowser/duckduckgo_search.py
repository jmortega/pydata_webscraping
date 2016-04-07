import re
from robobrowser import RoboBrowser

browser = RoboBrowser()
browser.open("https://duckduckgo.com")
# Must find the proper id in the html
form = browser.get_form(id = "search_form_homepage")
form
form["q"].value = "python"
browser.submit_form(form)
links = browser.get_links()
for link in links:
	print(link)