# -*- coding: utf-8 -*-
"""
# в терминале установить
pip install scrapy
# создание проекта scrapy
# наименование проекта
# расположение проекта
scrapy startproject jobparser .
# после формирования папок проекта требуется создать паука.
# название
# домен
scrapy genspider hhru hh.ru
# модуль необходимый для фотографий
pip install pillow
'''--------------------
Настройки хранятся в: settings.py
BOT_NAME - название
SPIDER_MODULES - где файл паука
NEWSPIDER_MODULE - где создавать новых пауков
USER_AGENT - UA, chrome://version/ - для Chrome
ROBOTSTXT_OBEY - получить данные robots.txt, оставить - false
CONCURRENT_REQUESTS - максимальное количество запросов за 1 такт, по умолчанию - 16 (можно закомментить)
DOWNLOAD_DELAY - пауза перед следующим сбором
COOKIES_ENABLED - хранить куки
ITEM_PIPELINES - после сбора item требуется обработка в piplines, если строка закомментирована, то не будет
LOG_ENABLED = True - включить логи
LOG_LEVEL = 'DEBUG' - уровень логов
IMAGES_STORE = 'images' - директория изображений
--------------------'''
scrapy запускается с командной строки
Но для отладки можно создать отдельный файл, например runner.py
"""
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# импорт настроек
from leroiparser import settings
# импорт паука
from leroiparser.spiders.leroymerlinru import LeroymerlinruSpider

if __name__ == '__main__':
    # объект настроек
    crawler_settings = Settings()
    # у объекта вызывается объект принимающий настройки
    crawler_settings.setmodule(settings)

    # передаваемый параметр паука
    query = 'kraski-dlya-sten-i-potolkov'

    # создание процесса, который будет выполнять работу
    process = CrawlerProcess(settings=crawler_settings)
    # указание какой паук(пауки) будет работать в рамках процесса
    # кроме класса передаются параметры, которые будут переданы конструктору
    process.crawl(LeroymerlinruSpider, catalog=query)

    # запуск процесса (всех пауков сразу)
    process.start()