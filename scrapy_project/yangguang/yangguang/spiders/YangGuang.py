# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem


class YangguangSpider(scrapy.Spider):
    name = 'YangGuang'
    allowed_domains = ['sun0769.com']
    start_urls = [
        'http://wz.sun0769.com/index.php/question/questionType?type=4']

    def parse(self, response):
        # print(response.)
        # 分组
        tr_list = response.xpath('//div[@id="morelist"]//table//table//tr')
        # print(len(tr_list))

        for tr in tr_list:
            item = YangguangItem()
            item['title'] = tr.xpath(
                './/a[@class="news14"]/text()').extract_first()
            item['author'] = tr.xpath('.//td[last()-1]/text()').extract_first()
            item['href'] = tr.xpath('.//td[2]/a[2]/@href').extract_first()
            item['status'] = tr.xpath(
                './/td[last()-2]/span/text()').extract_first()
            item['publish_time'] = tr.xpath(
                './/td[last()]/text()').extract_first()

            # 处理详情页
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                meta={"item": item}
            )

        # 构造下一页url
        page = response.xpath(
            '//div[@class="pagination"]/span/text()').extract_first()
        next_url = response.xpath(
            '//a[text()=">"]/@href').extract_first()
        if next_url is not None:
            print('第{}页成功'.format(page))
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):
        """处理详情页"""
        item = response.meta['item']
        item['content'] = response.xpath(
            '//div[@class="wzy1"]//td[1]/text()').extract()
        item['content_img'] = response.xpath(
            '//td[@class="txt16_3"]//img/@src').extract()
        item['content_img'] = ["http://wz.sun0769.com" +
                               i for i in item['content_img']]
        yield item
