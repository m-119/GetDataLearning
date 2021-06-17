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
--------------------'''

scrapy запускается с командной строки
Но для отладки можно создать отдельный файл, например runner.py
"""
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# импорт настроек
from jobparser import settings
# импорт паука
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperjobruSpider

if __name__ == '__main__':
    # объект настроек
    crawler_settings = Settings()
    # у объекта вызывается объект принимающий настройки
    crawler_settings.setmodule(settings)

    # создание процесса, который будет выполнять работу
    process = CrawlerProcess(settings=crawler_settings)
    # указание какой паук(пауки) будет работать в рамках процесса
    process.crawl(HhruSpider)
    process.crawl(SuperjobruSpider)

    # запуск процесса (всех пауков сразу)
    process.start()