from scrapy.selector import Selector

from slidebot.basespider import BaseSpider
from slidebot.items import SlideItem


class SlideshareSpider(BaseSpider):
    name = "slideshare"

    def parse(self, response):
        sel = Selector(response)
        og_url = sel.css('meta[name=og_url]::attr(content)').extract()[0]
        slide_id = og_url.rpartition('/')[2]
        return SlideItem(
            # this urls are already fully qualified
            id=slide_id,
            image_urls=sel.css('.slide_image::attr(data-normal)').extract(),
            url=og_url,
        )
