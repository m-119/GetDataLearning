# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroiparser.items import LeroiparserItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

'''
1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
● название;
● все фото;
● параметры товара в объявлении;
● ссылка;
● цена.

Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.

Дополнительно:
2)Написать универсальный обработчик характеристик товаров, который будет формировать данные вне зависимости от их типа и количества.
3)Реализовать хранение скачиваемых файлов в отдельных папках, каждая из которых должна соответствовать собираемому товару
'''
'''
CSS: 
название - ссылка: document.querySelectorAll('a[data-qa="product-name"]')
далее - ссылка: document.querySelectorAll('a[data-qa-pagination-item="right"]')
● название: document.querySelectorAll('h1')
● все фото: document.querySelectorAll('picture[slot="pictures"] > img')
● параметры товара в объявлении: document.querySelectorAll('dl[class="def-list"]')
● ссылка: *из ответа
● цена: document.querySelectorAll('uc-pdp-price-view[class="primary-price"] > span[slot="price"]')
ps фото присутствуют на странице сразу.
'''

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = [f'http://leroymerlin.ru/catalogue/kraski-dlya-sten-i-potolkov/']
    def __int__(self, catalog):
        # вызов конструктора родителя, в противном случае - консруктор перезатрется.
        super(LeroymerlinruSpider, self).__init__()
        # ссылки (или другие параметры) передаваемые для поиска
        # переменная перешла в метод, и стала
        # этот вариант не сработал
        # self.start_urls = [f'http://leroymerlin.ru/catalogue/{catalog}/']
        print()

    def parse(self, response: HtmlResponse):
        # не обязательно у <a> вытягивать адресс ссылки через xpath @href и .extract()
        # но, здесь этом моменте дебаггер непредсказуемо падает с ошибкой
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd1 in position 1023: unexpected end of data
        elements = response.css('a[data-qa="product-name"]').xpath('@href').extract()
        # for e in elements:
        #     yield response.follow(e, callback=self.parse_element)
        # Для решения извлек ссылки полностью
        for e in elements:
            yield response.follow(e, callback=self.parse_element)

    def parse_element(self, response: HtmlResponse):
        #объект класса лоадер, в который передается запрос и новый объект LeroiparserItem
        loader = ItemLoader(item=LeroiparserItem(), response=response)

        # теперь паук занимается парсингом
        loader.add_css('name', 'h1')
        loader.add_css('photos', 'picture[slot="pictures"] > img')
        loader.add_css('params', 'h1')
        loader.add_value('url', response.url)
        loader.add_css('price', 'uc-pdp-price-view[class="primary-price"] > span[slot="price"]')

        # обработка идёт в айтемах
        yield loader.load_item()


        # name = response.css('h1')
        # // picture[contains( @ slot, "pictures")] / descendant::img
        # photos = response.css('picture[slot="pictures"] > img').xpath('@src').extract()
        # params = response.css('dl[class="def-list"]')
        # url = response.url
        # price = int(re.sub(r'\s', '', BeautifulSoup(response.css('uc-pdp-price-view[class="primary-price"] > span[slot="price"]').extract_first()).text))
        # item = LeroiparserItem(name=name, photos=photos, params=params, url=url, price=price)
        # yield item