import json
from urlparse import urlparse

from scrapy.http import Request
from scrapy.selector import Selector

from slidebot.basespider import BaseSpider
from slidebot.items import SlideItem


class SpeakerdeckSpider(BaseSpider):
    name = "speakerdeck"
    player_url = 'https://speakerdeck.com/player/{hash}'

    def parse(self, response):
        sel = Selector(response)
        hash = sel.css('.speakerdeck-embed::attr(data-id)').extract()[0]
        return Request(self.player_url.format(hash=hash), callback=self.parse_player)

    def parse_player(self, response):
        sel = Selector(response)
        content = sel.xpath('/html/head/script[not(@src)]/text()').re(r'talk = (.+?);')[0]
        data = json.loads(content)
        pr = urlparse(data['url'])
        slide_id = pr.path.strip('/').replace('/', '_')
        return SlideItem(
            # this urls are already fully qualified
            id=slide_id,
            image_urls=[s['original'] for s in data['slides']],
            url=data['url'],
        )
