import scrapy


class MonclerItem(scrapy.Item):
    name = scrapy.Field()
    imgs = scrapy.Field()