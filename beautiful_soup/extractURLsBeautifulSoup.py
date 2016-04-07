#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests

url = raw_input("Enter a website to extract the URL's from: ")

r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data,"lxml")

for link in soup.find_all('a'):
    print(link.get('href'))