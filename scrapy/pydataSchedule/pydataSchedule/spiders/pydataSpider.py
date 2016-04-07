# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import BaseSpider
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader import XPathItemLoader
from pydataSchedule.items import PydatascheduleItem

class PydataspiderSpider(scrapy.Spider):
    name = "pydataSpider"
    allowed_domains = ["www.pydata.org"]
    start_urls = ['http://pydata.org/madrid2016/schedule/']

    def parse(self, response):
        hxs = scrapy.Selector(response)
        slots = hxs.xpath('//td[@class="slot slot-talk"]')
        for slot in slots:
            speakers = slot.xpath('//span[@class="speaker"]/text()').extract()
            urls = slot.xpath('//span[@class="title"]//@href').extract()
            talks = slot.xpath('//span[@class="title"]//a/text()').extract()
            
        i=0
        for speaker in speakers:
            yield PydatascheduleItem(speaker=speaker.strip(), url=urls[i], talk=talks[i])
            i=i+1
