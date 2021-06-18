# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from jobparser.items import JobparserItem
from lutils import salary as slr
from pymongo import MongoClient

class JobparserPipeline:
    def __int__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client['vacancies']
    def process_item(self, item, spider):
        salary = slr(item.get('salary'))
        item.update(salary)
        item.pop('salary')

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item
