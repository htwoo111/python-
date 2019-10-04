# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class BxjSpider(CrawlSpider):
    name = 'bxj'
    allowed_domains = ['hupu.com']
    start_urls = ['https://bbs.hupu.com/bxj']
    current_page = 0

    # 定义提取url地址的规则
    rules = (
        # linkextractor 提取url地址
        # callback 提取出来的url地址的response会交给callback处理
        # follow 当前url地址的响应是否能用rules来提取
        Rule(LinkExtractor(restrict_xpaths=['//a[@class="truetit"]']), callback='parse_item', follow=False),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        print(self.current_page)
        print('\n\n')
        if self.current_page == 50:
            return
        self.current_page += 1
        next_url = 'https://bbs.hupu.com/bxj-' + str(self.current_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse_item
        )



    def parse_item(self, response):
        # print(response)
        item = {}
        item['title'] = response.xpath('//h1[@id="j_data"]/text()').extract_first()
        item['content'] = response.xpath('//div[@class="quote-content"]//text()').extract()
        # #item['description'] = response.xpath('//div[@id="description"]').get()
        print(item)