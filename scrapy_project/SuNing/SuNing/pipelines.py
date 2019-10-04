# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class SuningPipeline(object):
    collection_name = 'suning_book'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_HOST'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items') 
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri, port=27017)
        self.collection = self.client[self.mongo_db][self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # print(item)
        self.collection.insert_one(dict(item))
        return item
