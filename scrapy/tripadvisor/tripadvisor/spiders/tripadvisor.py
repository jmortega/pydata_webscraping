# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import TripadvisorItem

class TripadvisorSpider(scrapy.Spider):
    name=  "tripadvisor"
    allowed_domains = ['tripadvisor.es']
    start_urls=['https://www.tripadvisor.es/Restaurants-g187497-Barcelona_Catalonia.html']
    
    #rules = [Rule(LxmlLinkExtractor(allow=['h3']),callback='process_response')]
    
    def parse(self,response):
        #process each link
        urls = response.xpath('//h3[@class="title"]/a/@href').extract()
        for url in urls:    
            absolute_url = response.urljoin(url)
	    print absolute_url
            yield scrapy.Request(absolute_url,callback=self.parse_restaurant)
	    
	#next_page 
	next_page_url = response.xpath('//a[text()="Next"]').extract_first()
	next_page_absolute_url = response.urljoin(next_page_url)
	yield scrapy.Request(next_page_absolute_url,callback=self.parse)

    def parse_restaurant(self, response):
	rating = response.xpath('//img[@property="ratingValue"]/@content').extract_first()
	name = response.xpath('//div[@class="mapContainer"]/@data-name').extract_first()
	latitude = response.xpath('//div[@class="mapContainer"]/@data-lat').extract_first()
	longitude = response.xpath('//div[@class="mapContainer"]/@data-lng').extract_first()
	url = response.url
	
	yield {'Rating' :rating,'name' :name,'latitude' :latitude,'longitude' :longitude,'url' :url}

    def process_response(self, response):
	item = TripadvisorItem()
	item['url'] = response.xpath('//h3[@class="title"]/a/@href').extract()
	return item