# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json
import urllib


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        print('parse...')
        item = {}
        # 获取大分类列表
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        # 遍历大分类列表获取每一个大分类
        for dt in dt_list:
            item['b_cate'] = dt.xpath('./a/text()').extract_first()
            # 获取到小分类列表
            em_list = dt.xpath('./following-sibling::dd[1]/em')
            # 遍历小分类列表获取每一个小分类
            for em in em_list:
                # 获取每一个小分类的名称
                item['s_cate'] = em.xpath('./a/text()').extract_first()
                # 获取每一个小分类的url
                item['s_href'] = em.xpath('./a/@href').extract_first()
                if item['s_href'] is not None:
                    # 补全url
                    item['s_href'] = 'https:' + item['s_href']
                    # 进入小分类详情页，获取图书
                    yield scrapy.Request(
                        item['s_href'],
                        callback=self.get_books,
                        # 由于是多线程，如果不深拷贝的话，数据会出现错乱
                        meta={'item': deepcopy(item)}
                    )

    def get_books(self, response):
        item = response.meta['item']
        # 获取所有图书的列表
        li_list = response.xpath('//div[@id="plist"]/ul/li')
        # 对图书列表进行遍历，获取每一本书的信息
        for li in li_list:
            item['book_img'] = li.xpath(
                './/div[@class="p-img"]//img/@src').extract_first()
            if item['book_img'] is None:
                item['book_img'] = li.xpath(
                    './/div[@class="p-img"]//img/@data-lazy-img').extract_first()
            if item['book_img'] is not None:
                item['book_img'] = 'https:' + item['book_img']
            item['book_name'] = li.xpath(
                './/div[@class="p-name"]/a/em/text()').extract_first().strip()
            item['book_press'] = li.xpath(
                './/span[@class="p-bi-store"]/a/text()').extract_first()
            item['book_author'] = li.xpath(
                './/span[@class="author_type_1"]/a/text()').extract()
            item['book_href'] = li.xpath(
                './/div[@class="p-name"]/a/@href').extract_first()
            item['book_publish_date'] = li.xpath(
                './/span[@class="p-bi-date"]/text()').extract_first().strip()
            item['data-sku'] = li.xpath('./div/@data-sku').extract_first()
            if item['book_href'] is not None:
                item['book_href'] = 'https:' + item['book_href']
            # 进入js页面，获取商品价格
            yield scrapy.Request(
                'https://p.3.cn/prices/mgets?&skuIds=J_{}'.format(
                    item['data-sku']),
                callback=self.get_book_price,
                meta={'item': deepcopy(item)}
            )

        # 构造下一页url
        next_url = response.xpath(
            '//a[@class="pn-next"]/@href').extract_first()
        # 判断是否存在下一页
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.get_books,
                meta={'item': item}
            )

    def get_book_price(self, response):
        item = response.meta['item']
        price = json.loads(response.body.decode('utf-8'))[0]['op']
        item['price'] = price
        # print(item)
        # 进入js页面，获取商品commentcount
        yield scrapy.Request(
            'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds={}'.format(
                item['data-sku']),
            callback=self.get_book_commentcount,
            meta={'item': deepcopy(item)}
        )

    def get_book_commentcount(self, response):
        item = response.meta['item']
        comment_count = json.loads(response.text)['CommentsCount'][0]['CommentCount']
        item['comment_count'] = comment_count   
        yield item        