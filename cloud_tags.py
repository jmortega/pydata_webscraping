import requests
import urllib
import json
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

words = ["python","scraping","tools","Python tools for webscraping"]
TEXT = '''I am trying to create a word cloud in python for pydata conference. Python tools for webscraping'''

text = "%s" % " ".join(words)	

counts = get_tag_counts(TEXT)
tags = make_tags(counts, maxsize=90)
create_tag_image(tags, 'cloud_tags.png', size=(1024, 860), fontname='Lobster')
