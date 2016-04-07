#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.settings import Settings
from scrapy import signals


class PydatascheduleItem(Item):
    # define the fields for your item here like:
	speaker = Field()
	url = Field()
	talk = Field()
	time = Field()
	description = Field()
    
class PydataSpiderDetails(CrawlSpider):
	name = "pydataSpider"
	allowed_domains = ["pydata.org"]
	start_urls = ['http://pydata.org/madrid2016/schedule/']
	rules = [Rule(LxmlLinkExtractor(allow=['presentation']), callback='parse_details')]


	def parse_details(self, response):
		print 'link parseado %s' %response.url		
		hxs = scrapy.Selector(response)
		item = PydatascheduleItem()
		item['speaker'] = hxs.select('//div[@class="col-md-8"]/h4/a/text()').extract()[0].strip()
		item['url'] = response.url
		item['talk'] = hxs.select('//div[@class="col-md-8"]/h2/text()').extract()[0].strip()
		item['time'] = hxs.select('//div[@class="col-md-8"]/h4/text()').extract()[0].replace("\n","").strip()
		item['description'] = hxs.select('//div[@class="description"]/p/text()').extract()[0]
		return item 

def main():
	from scrapy.xlib.pydispatch import dispatcher
	
	"""Rutina principal para la ejecución del Spider"""
	# set up signal to catch items scraped
	def catch_item(sender, item, **kwargs):
		print "Item extracted:", item
	dispatcher.connect(catch_item, signal=signals.item_passed)

	settings = Settings()
	settings.set("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36")
	settings.set("LOG_ENABLED",False)	

	# setup crawler
	from scrapy.crawler import CrawlerProcess

	crawler = CrawlerProcess(settings)

	# define spyder for the crawler
	crawler.crawl(PydataSpiderDetails())

	print "STARTING ENGINE"
	crawler.start() #start  the crawler
	print "ENGINE STOPPED"

if __name__ == '__main__':
	main()
