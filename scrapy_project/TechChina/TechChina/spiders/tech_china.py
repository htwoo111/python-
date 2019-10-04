# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TechChina.items import TechchinaItem


class TechChinaSpider(CrawlSpider):
    name = 'tech_china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article/\d+/.*\.html',
                           restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@id="pageStyle"]/a[@class="a1"]'), follow=True)
    )

    def parse_item(self, response):
        item = TechchinaItem()
        item['title'] = response.xpath(
            '//h1[@id="chan_newsTitle"]/text()').extract_first()
        item['datetime'] = response.xpath(
            '//div[@id="chan_newsInfo"]/text()').re_first(r'\d{4}-\d{2}-\d{2}.*\d')
        # item['text'] = ''.join(response.xpath('//div[@id="chan_newsDetail"]//text()').extract()).strip()
        item['url'] = response.url
        item['website'] = '中华网'
        item['source'] = response.xpath(
            '//div[@id="chan_newsInfo"]/text()').re_first(r'来源：(.*)').strip()
        print(item)
        yield item
