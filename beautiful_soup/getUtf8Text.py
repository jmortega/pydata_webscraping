import requests
from bs4 import BeautifulSoup

html = requests.get("http://en.wikipedia.org/wiki/Python_(programming_language)").text
bsObj = BeautifulSoup(html)
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
content = bytes(content.encode('UTF-8'))
content = content.decode("UTF-8")
print(content.encode('UTF-8'))