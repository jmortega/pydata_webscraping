# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import BaseSpider
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader import XPathItemLoader
from scrapy.http import Request
from pydataSchedule.items import PydatascheduleItem

class PydataspiderSpiderDetails(scrapy.Spider):
    name = "pydataSpiderDetails"
    allowed_domains = ["www.pydata.org"]
    start_urls = ['http://pydata.org/madrid2016/schedule/']

    def parse(self, response):
        hxs = scrapy.Selector(response)
        slots_tutorials = hxs.xpath('//td[@class="slot slot-tutorial"]')
        for slot in slots_tutorials:
            speakers_tutorials = slot.xpath('//span[@class="speaker"]/text()').extract()
            urls_tutorials = slot.xpath('//span[@class="title"]//@href').extract()
            talks_tutorials = slot.xpath('//span[@class="title"]//a/text()').extract()
            
        indexSpeaker=0
        for speaker in speakers_tutorials:
            yield Request(url=''.join(('http://www.pydata.org', urls_tutorials[indexSpeaker])),
                          callback=self.parse_details,
                          meta={'speaker': speaker.strip(), 'url': urls_tutorials[indexSpeaker], 
						  'talk': talks_tutorials[indexSpeaker]}
                          )       
            indexSpeaker=indexSpeaker+1        

    def parse_details(self, response):
        hxs = scrapy.Selector(response)
        item = PydatascheduleItem()
        item['speaker'] = response.meta['speaker'].encode('utf8')
        item['url'] = response.meta['url'].encode('utf8')
        item['talk'] = response.meta['talk'].encode('utf8')
        item['time'] = hxs.xpath('//div[@class="col-md-8"]/h4/text()').extract()[0].replace("\n","").strip().encode('ascii', 'ignore').encode('utf8')
        item['description'] = hxs.xpath('//div[@class="description"]/p/text()').extract()[0].encode('utf-8')
        return item    