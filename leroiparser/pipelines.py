# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class LeroiparserPipeline:
    def process_item(self, item, spider):
        return item

class LeroiparserImagesPipeline(ImagesPipeline):
    # в настройках ITEM_PIPELINES указывается приоритет пайплайнов
    def get_media_requests(self, item, info):
        # есть ли что-то в списке фотографий
        if item.fields['photos']:
            # роходимся по списку
            for img in item.fields['photos']:
                try:
                    # дополнительный запрос по ссылке с фото
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    # переопределение метода требуется для именования полученных файлов
    def item_completed(self, results, item, info):
        # если список кортежей с информацией о файлах есть
        if results:
            # айтемы делаются словарями, если статус True
            item.fields['photos'] = [itm[1] for itm in results if itm[0]]
        # возвращает айтем в основной пайплайн
        return item