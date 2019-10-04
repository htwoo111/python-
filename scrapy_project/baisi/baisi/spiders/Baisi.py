# -*- coding: utf-8 -*-
import scrapy
from baisi.items import BaisiItem


class BaisiSpider(scrapy.Spider):
    name = 'Baisi'
    allowed_domains = ['budejie.com']
    start_urls = ['http://budejie.com/']

    def parse(self, response):
        if response.status != 200:
            return
        li_list = response.xpath('//div[@class="j-r-list"]/ul/li')
        # print(len(li_list))
        print(response.status)
        for li in li_list:
            # item = {}
            item = BaisiItem() 
            item['user_name'] = li.xpath(
                './/div[@class="j-list-user"]//a[@class="u-user-name"]/text()').extract_first()
            item['title'] = li.xpath(
                './/div[@class="j-r-list-c-desc"]/a/text()').extract_first()
            item['publish_time'] = li.xpath(
                './/div[@class="u-txt"]/span[contains(@class, u-time)]/text()').extract_first()
            item['href'] = "http://budejie.com" + li.xpath('.//div[@class="j-r-list-c-desc"]/a/@href').extract_first()
            yield item

        # 构造下一个url
        # next_url = "http://budejie.com/" + response.xpath('//a[@class="pagenxt"]/@href').extract_first()
        # yield scrapy.Request(
        #     next_url, 
        #     callback=self.parse   # 如果下一页url与当前的不一样则需要重新写一个parse2
        # )