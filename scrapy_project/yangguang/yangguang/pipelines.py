# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from yangguang.items import YangguangItem
import re

client = MongoClient()
collection = client['yangguan']['yg1']


class yangguangPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, YangguangItem):
            item = dict(item)
            item['content'] = self.process_content(item['content'])

            # 根据url进行去重
            href = item.get('href')
            try:
                if collection.find_one({"href": href}):
                    collection.update_one({"href": href}, {"$set": item})
                    # print('更新成功')
                else:
                    collection.insert_one(item)
                    # print('插入成功')
            except Exception as e:
                print('error : {}'.format(e))
        return item
    def process_content(self, content_list):
        content_list = [re.sub(r"\xa0|\s", "", i) for i in content_list]
        content_list = [i for i in content_list if len(i)>0]
        return content_list
