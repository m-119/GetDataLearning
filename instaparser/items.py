# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    source_name = scrapy.Field()
    source_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_fullname = scrapy.Field()
    photo = scrapy.Field()
    subs_type = scrapy.Field()
