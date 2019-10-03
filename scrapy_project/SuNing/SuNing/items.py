# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    b_cate = scrapy.Field()
    s_cate = scrapy.Field()
    third_cate = scrapy.Field()
    book_href = scrapy.Field()
    comment_count = scrapy.Field()
    third_cate_href = scrapy.Field()
    category_id = scrapy.Field()