# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class LeruaparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.lerua

    def process_item(self, item, spider):
        item['name'] = item['name']
        item['url'] = item['url']
        item['price'] = float(item['price'])
        item['_id'] = int(item['_id'][0])

        collection = self.mongobase[spider.name]
        try:
            collection.update_one({'_id': item['_id']}, {'$set': item}, upsert=True)
        except DuplicateKeyError as e:
            print(e, item['_id'])
        return item


class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        print()
    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'full/{item["_id"]}/{request.url.split("/")[-1]}'
