import scrapy
from scrapy.http import HtmlResponse

from bs4 import BeautifulSoup
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
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
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # все ссылки которые требуется обработать (точки входа) 1 на поток, ссылка уходит в response
    start_urls = [
        'https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=Python']

    def parse(self, response: HtmlResponse):
        # перейти на следующую страницу и вызвать сбор
        next_page = response.css('a[data-qa="pager-next"]').xpath('@href').extract_first()
        yield response.follow(next_page, self.parse)
        # получение списка элементов и ссылки через .extract()
        # сначала по CSS, потом по XPATH, т.к. не уверен что CSS врожденно может получать значение тега
        vacancies = response.css('a[data-qa="vacancy-serp__vacancy-title"]').xpath('@href').extract()
        for e in vacancies:
            # сохраняем состояние методов
            # у респонса вызываем метод выполняющий передачу объекта в метод
            yield response.follow(e, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        # проверить на какой ссылке в настоящий момент
        # response.url
        try:
            title_ = BeautifulSoup(response.xpath('//*[@data-qa="vacancy-title"]').extract_first(), 'lxml').text
        except:
            title_ = None

        try:
            salary_ = BeautifulSoup(response.xpath('//*[@class="vacancy-salary"]').extract_first(), 'lxml').text
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
