#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys

#Example input to enter : en (= english)
convert_from = raw_input("Language to Convert from : ")

#Example input to enter : es (= spanish)
convert_to = raw_input("Language to Convert to : ")

text_to_convert = raw_input("Texto a traducir: ")

#remplazar espacios por el signo +
text_to_convert = text_to_convert.replace(' ', '+')

#llamar al servicio de translate
url = 'https://translate.google.com/?sl=%s&tl=%s&text=%s' % (convert_from, convert_to, text_to_convert)

#obtener respuesta
data = requests.get(url,verify=False).content

soup = BeautifulSoup(data, "lxml")

#obtener resultados de traduccion
div_content = soup.find('div', {'id' : 'gt-res-content'})

converted_text = div_content.find('span', {'id':'result_box'}).text

print "Texto traducido : " + converted_text
