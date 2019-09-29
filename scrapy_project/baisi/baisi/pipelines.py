# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

client = MongoClient()
collection = client['baisibudejie']['baisi1']


class BaisiPipeline(object):
    def process_item(self, item, spider):
        href = item.get('href')
        try:
            if collection.find_one({"href": href}):
                collection.update_one({"href": href}, {"$set": {item}})
            else:
                collection.insert_one(item)
        except Exception as e:
            print('error : {}'.format(e))
        print(item)
