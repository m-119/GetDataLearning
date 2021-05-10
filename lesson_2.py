#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import lxml.html
import re
import pandas as pd
from lxml.etree import Element

text: None
while True:
    text = input("поиск вакансии по слову:")
    if len(text) < 3:
        print("Запрос меньше 3х символов")
    else:
        break

result = []

import codecs


def strict_handler(exception):
    return u"", exception.end


codecs.register_error("strict", strict_handler)


def decode(s, encoding="ascii", errors="ignore"):
    return s.decode(encoding=encoding, errors=errors)


def setup_coder(enc: str = None, dec: str = None):
    _enc: str = None
    _dec: str = None

    def stub(s: str):
        return s

    def coder(s: str):
        return s.encode(_enc).decode(_dec).strip()

    if (not enc) and (not dec):
        return stub
    else:
        _enc = 'utf8' if enc == None else enc
        _dec = 'utf8' if dec == None else dec
        return coder


def salary(s: str) -> dict:
    curency: dict = {"бел. руб.": "BEL", "руб": "RUB", "usd": "USD", "eur": "EUR", "kzt": "KZT"}
    result = {"min": "", "stable": "", "max": "", "curr": ""}

    r_digits = re.compile('\d+', re.IGNORECASE)
    r_min = re.compile('от', re.IGNORECASE)
    r_max = re.compile('до', re.IGNORECASE)
    r_curency = re.compile(f'({"|".join(list(curency.keys()))})', re.IGNORECASE)

    if s is None:
        return result

    sr = re.sub(r'\s+', '', s).lower()
    min_max = r_digits.findall(sr)

    if len(min_max) == 1:
        if r_min.findall(sr):
            result["min"] = min_max[0]
        elif r_max.findall(sr):
            result["max"] = min_max[0]
        else:
            result["stable"] = min_max[0]
    elif len(min_max) == 2:
        result["min"] = min_max[0]
        result["max"] = min_max[1]
    c = r_curency.search(sr)
    if c:
        result["curr"] = curency[c.group(0)]
    return result


sites: dict = {'hh.ru':
                   {"search": r"/search/vacancy/",
                    "next": r"//*[text()='дальше']/ancestor::a",
                    "next_link": r"//*[@d='M8.59 16.34l4.58-4.59-4.58-4.59L10 5.75l6 6-6 6z']/ancestor::a",
                    "keyword": "text",
                    "vacancies": "//div[@data-qa = 'vacancy-serp__results']/div[contains(@class, 'vacancy-serp-item')]",
                    "name": ".//*[@data-qa = 'vacancy-serp__vacancy-title']",
                    "salary": ".//*[@data-qa = 'vacancy-serp__vacancy-compensation']",
                    "company": ".//*[@data-qa = 'vacancy-serp__vacancy-employer']"
                    },
               "superjob.ru":
                   {"search": r"/vacancy/search/",
                    "next": r"//*[text()='Дальше']/ancestor::a",
                    "next_link": r"//*[@d='M8.59 16.34l4.58-4.59-4.58-4.59L10 5.75l6 6-6 6z']/ancestor::a",
                    "keyword": "keywords",
                    "vacancies": "//*[@class = 'Fo44F QiY08 LvoDO']",
                    "name": ".//*[@class = '_1h3Zg _2rfUm _2hCDz _21a7u']/a",
                    "salary": ".//*[contains(@class, 'f-test-text-company-item-salary')]",
                    "company": ".//*[contains(@class, 'f-test-text-vacancy-item-company-name')]/a"
                    },
               'www.rabota.ru':
                   {"search": r"",
                    "next": r"//*[@d='M8.59 16.34l4.58-4.59-4.58-4.59L10 5.75l6 6-6 6z']/ancestor::a",
                    "next_link": r"//*[@d='M8.59 16.34l4.58-4.59-4.58-4.59L10 5.75l6 6-6 6z']/ancestor::a",
                    "keyword": "query",
                    "attrs": {"sort": "relevance"},
                    "vacancies": "//*[@class = 'vacancy-preview-card__top']",
                    "name": ".//*[@class = 'vacancy-preview-card__title']/a",
                    "salary": ".//*[contains(@class, 'vacancy-preview-card__salary')]/a",
                    "company": ".//*[@class = 'vacancy-preview-card__company-name']/a",
                    "encode": "iso-8859-1",
                    "decode": "utf8"
                    # .encode('iso-8859-1').decode('utf8')
                    },
               # лимит на количество записей
               'limit': 100
               }
params = {'text': 'a'}
headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

for site in list(sites.keys()):
    # ограничение для контроля количества возвращаемых значений
    limit = sites['limit']
    if site == 'limit':
        # c работа.ру не срослось.
        break;
    coder = setup_coder(sites[site].get("encode"), sites[site].get("decode"))
    link = sites[site]["search"]
    params = {sites[site]["keyword"]: text}
    if sites[site].get("attrs"):
        params.update(sites[site].get("attrs"))
    while True:
        response = requests.get(f"http://{site}{link}", params=params, headers=headers, stream=True)
        response.raw.decode_content = True
        tree = lxml.html.parse(response.raw)

        for e in tree.xpath(sites[site]["vacancies"]):
            print(response.url)
            d = {"site": site, "company": "", "name": "", "min": "", "stable": "", "max": "", "curr": ""}
            if len(e.xpath(sites[site]["name"])):
                # print(tostring(e.xpath(sites[site]["name"])[0]))
                # print(e.xpath(sites[site]["name"])[0].text_content())
                d["name"] = re.sub(r'\s+', ' ', coder(e.xpath(sites[site]["name"])[0].text_content()))
            if len(e.xpath(sites[site]["salary"])):
                # print(tostring(e.xpath(sites[site]["salary"])[0]))
                # print(e.xpath(sites[site]["salary"])[0].text_content())
                d.update(salary(coder(e.xpath(sites[site]["salary"])[0].text_content())))
            if len(e.xpath(sites[site]["company"])):
                # print(tostring(e.xpath(sites[site]["company"])[0]))
                # print(e.xpath(sites[site]["company"])[0].text_content())
                d["company"] = re.sub(r'\s+', ' ', coder(e.xpath(sites[site]["company"])[0].text_content()))
            result.append(d)
            limit -= 1
            if not limit: break
        if not limit: break

        params = None
        link = tree.xpath(sites[site]["next"])

        if link:
            link = tree.xpath(sites[site]["next"])[0].attrib.get('href')
        else:
            break
df = pd.DataFrame(result)
print(df)

# pprint(len(serials_list))
