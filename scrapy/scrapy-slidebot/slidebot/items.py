from scrapy.item import Item, Field


class SlideItem(Item):
    id = Field()  # slide identifier
    image_urls = Field()
    images = Field()
    pdf_file = Field()
    spider = Field()
    url = Field()
