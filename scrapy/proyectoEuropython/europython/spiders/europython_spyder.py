# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from europython.items import EuropythonItem


class EuropythonSpyderSpider(CrawlSpider):
	name = "europython_spyder"
	allowed_domains = ["ep2015.europython.eu"]
	start_urls = ['http://ep2015.europython.eu/en/events/sessions']
	
	# Patrón para las entradas que cumplan el formato conference/talks
	rules = [Rule(LxmlLinkExtractor(allow=['conference/talks']),callback='process_response')]

	def process_response(self, response):
		item = EuropythonItem()
		print response
		item['title'] = response.xpath("//div[contains(@class, 'grid-100')]//h1/text()").extract()
		item['author'] = response.xpath("//div[contains(@class, 'talk-speakers')]//a[1]/text()").extract()
		item['description'] = response.xpath("//div[contains(@class, 'cms')]//p//text()").extract()
		item['date'] = response.xpath("//section[contains(@class, 'talk when')]/strong/text()").extract()
		item['tags'] = response.xpath("//div[contains(@class, 'all-tags')]/span/text()").extract()
		
		return item
