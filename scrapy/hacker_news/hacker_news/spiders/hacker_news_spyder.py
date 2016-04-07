# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from hacker_news.items import HackerNewsItem


class HackerNewsSpyder(CrawlSpider):
	name = "hacker_news_spyder"
	allowed_domains = ["news.ycombinator.com"]
	start_urls = ['https://news.ycombinator.com']
	
	def parse(self, response):
		hxs = Selector(response)
		urls = hxs.xpath('//a')
		items = []
		print urls
		for url in urls:
			item = HackerNewsItem()
			print url
			item['name'] = map(unicode.strip, url.select('text()').extract())
			item['link'] = map(unicode.strip, url.select('@href').extract())
			items.append(item)
		return items
