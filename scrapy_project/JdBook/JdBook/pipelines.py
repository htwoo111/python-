# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JdbookPipeline(object):
    client = MongoClient()
    collection = client['JdBook']['jd_book']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        print('插入数据成功')
        return item
