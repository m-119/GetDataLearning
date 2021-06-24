# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from bs4 import BeautifulSoup
from itemloaders.processors import MapCompose, TakeFirst

def s_prise(e) -> int:
    result = None
    try:
        result = int(re.sub(r'\s', '', BeautifulSoup(e).extract_first()).text)
    except:
        pass
    return result

def s_text(e) -> str:
    result = None
    try:
        result = re.sub(r'\s', '', BeautifulSoup(e).text)
    except:
        pass
    return result

def s_photos(e):
    result = None
    try:
        result = re.sub(r'\s', '', e.xpath('@src').extract())
    except:
        pass
    return result

class LeroiparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(s_text))
    photos = scrapy.Field(input_processor=MapCompose(s_photos))
    params = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(s_prise))

    # name = response.css('h1')
    # // picture[contains( @ slot, "pictures")] / descendant::img
    # photos = response.css('picture[slot="pictures"] > img').xpath('@src').extract()
    # params = response.css('dl[class="def-list"]')
    # price = int(re.sub(r'\s', '', BeautifulSoup(response.css('uc-pdp-price-view[class="primary-price"] > span[slot="price"]').extract_first()).text))
    # item = LeroiparserItem(name=name, photos=photos, params=params, url=url, price=price)
    # yield item

    pass
