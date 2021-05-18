from pymongo import MongoClient
#from lesson_2 import *
# # #
from pymongo.collection import Collection
from pymongo.database import Database

client = MongoClient('127.0.0.1', 27017)

db: Database = client['vacancies']

vacancies: Collection = db.vacancies

# vacancies.create_index([("site", 1), ("company", 1), ("name", 1), ("min", 1), ("stable", 1), ("max", 1), ("curr", 1)],
#                        unique=True, name='indx')
# vacancies.drop_index('indx')


def insert(l: list) -> None:
    """
    # 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
    записывающую собранные вакансии в созданную БД.
    вставка
    :param l: список для вставки
    :return:
    """
    vacancies.insert_many(l)


def search(s: str = None):
    """
    # 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
    больше введённой суммы.
    :param s:значение для поиска
    :return:
    """
    if s is None:
        s = input("Заработная плата больше:")
    if s.isdigit():
        s = int(s)
    else:
        print("<не число>")
    for e in vacancies.find({'$or': [{'min': {'$gt': s}}, {'stable': {'$gt': s}}, {'max': {'$gt': s}}]}):
        print(e)


def insert_unique(l: list) -> None:
    """
    # 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
    вставка уникальных
    :param l: список для вставки
    :return:
    """
    for e in l:
        if not vacancies.find_one(e):
            vacancies.insert_one(e)
        else:
            print('-: ', e)


print(search)

#insert_unique(result)
search()
# insert_unique(result)
# insert(result)
print(vacancies.find_one({'user_id': 211, 'name': 'Lukde'}))
pass
