import scrapy
from scrapy.http import HtmlResponse

from bs4 import BeautifulSoup
from jobparser.items import JobparserItem

class SuperjobruSpider(scrapy.Spider):
    """
    Урок 6. Scrapy
    1) Доработать паука в имеющемся проекте, чтобы он формировал item по структуре:
    *Наименование вакансии

    *Зарплата от
    *Зарплата до
    *Ссылку на саму вакансию

    *Сайт откуда собрана вакансия
    И складывал все записи в БД(любую)
    """
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    # все ссылки которые требуется обработать (точки входа) 1 на поток, ссылка уходит в response
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        # перейти на следующую страницу и вызвать сбор
        next_page = response.xpath('//span[contains(text(),"Дальше")]/ancestor::a/@href').extract_first()
        yield response.follow(next_page, self.parse)
        # получение списка элементов и ссылки через .extract()
        # сначала по CSS, потом по XPATH, т.к. не уверен что CSS врожденно может получать значение тега
        vacancies = response.xpath('.//*[@class = "_1h3Zg _2rfUm _2hCDz _21a7u"]/a/@href').extract()
        for e in vacancies:
            # сохраняем состояние методов
            # у респонса вызываем метод выполняющий передачу объекта в метод
            yield response.follow(e, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        # проверить на какой ссылке в настоящий момент
        # response.url
        try:
            title_ = BeautifulSoup(response.xpath('//h1').extract_first(), 'lxml').text
        except:
            title_ = None

        try:
            salary_ = BeautifulSoup(response.xpath('//span[@class="_1h3Zg _2Wp8I _2rfUm _2hCDz"]').extract_first(), 'lxml').text
        except:
            salary_ = None

        try:
            link_ = response.url
        except:
            link_ = None

        try:
            site_ = response.meta['download_slot']
        except:
            site_ = None

        item = JobparserItem(title=title_, salary=salary_, link=link_, site=site_)
        yield item
