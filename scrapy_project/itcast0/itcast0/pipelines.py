# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo


logger = logging.getLogger(__name__)


class Itcast0Pipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        print('init ...')
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        print('class method....')
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONG_DB')
        )

        def open_spider(self, spider):
            print('open spider...')
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if spider.name == 'itcast':
            logger.warning('*'*50)
        return item

    def close_spider(self, spider):
        self.client.close()
