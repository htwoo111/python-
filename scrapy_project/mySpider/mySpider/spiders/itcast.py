# -*- coding: utf-8 -*-
import scrapy


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        # 处理start_url 对应的响应
        # ret1 = response.xpath('//div[@class="tea_con"]//h3/text()')
        # print(ret1.extract())
        # print(type(ret1))

        
        li_list = response.xpath('//div[@class="tea_con"]//li')
        # print(li_list)
        for li in li_list:
            item = {}
            # item['name'] = li.xpath('.//h3/text()').extract()[0]
            item['name'] = li.xpath('.//h3/text()').extract_first()
            # item['title'] = li.xpath('.//h4/text()').extract()[0]
            item['title'] = li.xpath('.//h4/text()').extract_first()
            print("item:")
            yield item