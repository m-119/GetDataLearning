import requests
import lxml.html
import re
from datetime import datetime, timedelta
from dateutil import parser
from pymongo import MongoClient
# # #
from pymongo.collection import Collection
from pymongo.database import Database


def get_date(s: str):
    ystd = re.compile('вчера')
    month = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12}
    # format1 = re.compile('[^\d]*(\d+) (\w+) (\d+)')
    format2 = re.compile('(\d+) (\S+) ')
    s.replace(' в ', ' ')

    # вчера
    if ystd.search(date):
        return (datetime.now() - timedelta(days=1))
    elif format2.search(date):
        m = format2.match(date)
        return parser.parse(f"{m.group(1)}.{month.get(m.group(2))}")

    else:
        return datetime.now()

        # название источника;
    # наименование новости;
    # ссылку на новость;
    # дата публикации.


sources: dict = {
    # c mail.ru сложности, даты нормальны только в RSS, но там маленький список, проще отдельно:
    # пройтись по тематикам и везде получить RSS
    # проблема 2: там не названия а краткое содержание новостей
    # к тому же потребуется более сложный вариант с "1-8 часов назад" - регулярками и вычислениями

    #     'mail.ru':{
    #     'link': 'https://news.mail.ru',
    #     'news_name': '',
    #     'news_link': '',
    #     'news_date': ''
    # },
    'lenta.ru': {
        'link': 'https://lenta.ru/rss',
        'item': './/item',
        'news_name': './title',
        'news_link': './enclosure',
        'news_date': './pubdate'
    },
    'yandex.ru': {
        'link': 'https://yandex.ru/news',
        'item': './/div[contains(@class,"mg-grid__row")]/descendant::article',
        'news_name': '/descendant::*[@class="mg-card__title"]',
        'news_link': './descendant::a',
        'news_date': './descendant::*[@class="mg-card-source__time"]'
    }
}

headers: dict = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
result: list = []
name, link, date = '', '', ''
# для каждой из полученнных записей извлекается значение
for site in list(sources.keys()):
    response = requests.get(f"{sources.get(site).get('link')}", headers=headers, stream=True)
    response.raw.decode_content = True
    tree = lxml.html.parse(response.raw)
    for e in tree.xpath(sources.get(site).get('item')):

        # наименование новости;
        try:
            name = e.xpath(sources.get(site).get('news_name'))[0].text_content()
        except:
            name = None

        # ссылку на новость;
        try:
            link = e.xpath(sources.get(site).get('news_link'))[0].text_content()
        except:
            link = None

        # дата публикации.
        date = e.xpath(sources.get(site).get('news_date'))[0].text_content()
        try:
            date = parser.parse(date).date()
        except:
            date = get_date(date).date()
        # касаемо источника: точного указания не было: источник сайт, или источник, как указано на странице
        # во втором случае - это небольшое дополнение
        result.append({'source': site,
                       'name': name,
                       'link': link,
                       'date': date})

### запись в БД ###
client = MongoClient('127.0.0.1', 27017)

db: Database = client['news']

news: Collection = db.news

news.insert_many(result)
