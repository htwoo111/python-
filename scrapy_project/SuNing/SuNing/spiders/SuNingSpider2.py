# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from SuNing.items import SuningItem


class SuningspiderSpider(scrapy.Spider):
    name = 'SuNingSpider2'
    allowed_domains = ['suning.com']
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
        # inherit item for previous url
        item = response.meta['item']
        # get category id preparing for constructing next url
        item['category_id'] = response.xpath('//script').re(r'"categoryId":\s"(\d+)"')[
            0] if len(response.xpath('//script').re(r'"categoryId":\s"(\d+)"')) > 0 else None

        # get current page  preparing for constructing next url
        # current_page = response.xpath('//script').re(r'currentPage = "(\d+)"')[0] if len(
        #     response.xpath('//script').re(r'currentPage = "(\d+)"')) > 0 else None
        # get  page total  preparing for ending spider
        page_numbers = response.xpath('//script').re(r'pageNumbers = "(\d+)"')[0] if len(
            response.xpath('//script').re(r'pageNumbers = "(\d+)"')) > 0 else None

        print('goods_info_url')
        # yield url of goods info
        goods_info_url = "https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp=0".format(
            item['category_id'])
        yield scrapy.Request(
            goods_info_url,
            callback=self.get_book_info,
            meta={'item': deepcopy(item), 'page_numbers': page_numbers}
        )

    def get_book_info(self, response):
        print('start get book info')
        print(response.url)
        item = response.meta['item']
        page_numbers = response.meta['page_numbers']
        current_page = response.xpath('//script').re(r'currentPage = "(\d+)"')[0] if len(
            response.xpath('//script').re(r'currentPage = "(\d+)"')) > 0 else None
        print('current_page is {}'.format(current_page))
        print('\n\n')
        print('page_number is {}'.format(page_numbers))
        # get book li which contain all books info
        book_lis = response.xpath('//li[contains(@class, "product")]')
        for book_li in book_lis:
            item['title'] = book_li.xpath(
                './/p[@class="sell-point"]/a/text()').extract_first()
            item['book_href'] = "https:" + \
                book_li.xpath(
                    './/p[@class="sell-point"]/a/@href').extract_first()
            item['comment_count'] = book_li.xpath(
                './/p[@class="com-cnt"]/a/text()').extract_first()
            yield item

        # get more books info
        more_goods_info_url = response.url + '&paging=1'
        yield scrapy.Request(
            more_goods_info_url,
            callback=self.get_more_book_info,
            meta={'item': item, 'page_numbers': page_numbers,
                  'current_page': current_page}
        )

    def get_more_book_info(self, response):
        print('start get more book info')
        print('\n\n')
        print('\n\n')
        print(response.url)
        item = response.meta['item']
        page_numbers = response.meta['page_numbers']
        current_page = response.meta['current_page']
        # get book li which contain all books info
        book_lis = response.xpath('//li[contains(@class, "product")]')
        for book_li in book_lis:
            item['title'] = book_li.xpath(
                './/p[@class="sell-point"]/a/text()').extract_first()
            item['book_href'] = "https:" + \
                book_li.xpath(
                    './/p[@class="sell-point"]/a/@href').extract_first()
            item['comment_count'] = book_li.xpath(
                './/p[@class="com-cnt"]/a/text()').extract_first()
            yield item

        # construct next url
        if int(current_page) < int(page_numbers)-1:
            current_page = int(current_page) + 1
            next_url = response.url[:-10] + str(current_page)
            yield scrapy.Request(
                next_url,
                callback=self.get_book_info,
                meta={'item': item, 'page_numbers': page_numbers}
            )
