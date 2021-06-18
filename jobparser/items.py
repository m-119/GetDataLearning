# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    min = scrapy.Field()
    stable = scrapy.Field()
    max = scrapy.Field()
    currency = scrapy.Field()
    link = scrapy.Field()
    site = scrapy.Field()
    _id = scrapy.Field()
    pass
