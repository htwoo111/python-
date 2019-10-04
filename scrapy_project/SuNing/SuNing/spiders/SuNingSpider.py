# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from SuNing.items import SuningItem


class SuningspiderSpider(scrapy.Spider):
    name = 'SuNingSpider'
    allowed_domains = ['suning.com', 'baidu.com']
    start_urls = ['http://book.suning.com/']

    def parse(self, response):
        # extract the fitst heading list
        print(response.status)
        # print(response.body)
        heading_first_list = response.xpath(
            '//div[@class="menu-item"]//h3//text()').extract()  # return a list of first heading
        for heading_first in heading_first_list:
            index = heading_first_list.index(heading_first)
            # item = {}
            item = SuningItem()
            # 1.get first heading
            item['b_cate'] = heading_first
            # 2.get second heading
            # 2.1track second heading parent tag
            menu_sub_list = response.xpath(
                '//div[@class="menu-sub"]/div[@class="submenu-left"]')[:-1]
            # 2.2get second heading and href
            second_heading_info = menu_sub_list[index].xpath('./p/a')
            if len(second_heading_info) == 0:
                second_heading_info = ' '
            for heading_second in second_heading_info:
                third_heading_li = menu_sub_list[index].xpath('./ul/li')
                if second_heading_info != " ":
                    item['s_cate'] = heading_second.xpath(
                        './text()').extract_first()
                    # item['href'] = heading_second.xpath('./@href').extract_first()
                else:
                    item['s_cate'] = None
                    # item['href'] = None

                # 3. get third heading
                for third_heading in third_heading_li:
                    item['third_cate'] = third_heading.xpath(
                        './a/text()').extract_first()
                    item['third_cate_href'] = third_heading.xpath(
                        './a/@href').extract_first()
                    # print('\n\n')
                    if item['third_cate_href'] is not None:
                        yield scrapy.Request(
                            item['third_cate_href'],
                            # "https://www.baidu.com",
                            callback=self.get_book,
                            meta={'item': deepcopy(item)}
                        )

    def get_book(self, response):
        item = response.meta['item']
        item['category_id'] = response.xpath('//script').re(r'"categoryId":\s"(\d+)"')[
            0] if len(response.xpath('//script').re(r'"categoryId":\s"(\d+)"')) > 0 else None
        current_page = response.xpath('//script').re(r'currentPage = "(\d+)"')[0] if len(
            response.xpath('//script').re(r'currentPage = "(\d+)"')) > 0 else None
        book_lis = response.xpath('//div[@id="filter-results"]//ul/li')
        # print('end')
        for book_li in book_lis:
            item['title'] = book_li.xpath(
                './/p[@class="sell-point"]/a/text()').extract_first().strip()
            # item['price'] = book_li.xpath('.//p[@class="prive-tag]/em//text()"]').extract_first()
            item['book_href'] = 'https:' + \
                book_li.xpath(
                    './/p[@class="sell-point"]/a/@href').extract_first()
            item['comment_count'] = book_li.xpath(
                './/p[@class="com-cnt"]/a/text()').extract_first()
            yield item

        current_page += 1
        next_url = "https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}".format(item['category_id'], current_page)
        
