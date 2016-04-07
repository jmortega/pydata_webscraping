import requests
import re

web =  raw_input("Url: ")

response = requests.get('http://'+web).text

#regular expression for emails
pattern = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")

smails = re.findall(pattern,response)
print smails
mail_list = open ('emails.txt', 'wb')
d2 = str(smails)
mail_list.write(d2)
mail_list.close()
print "e-mails saved in file emails.txt"
