# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaisiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    user_name = scrapy.Field()
    publish_time = scrapy.Field()
    href = scrapy.Field()


class BaisiItem2(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    user_name = scrapy.Field()
    publish_time = scrapy.Field()
    href = scrapy.Field()
