import scrapy


class GlassonsItem(scrapy.Item):
    order = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    imgs_src = scrapy.Field()