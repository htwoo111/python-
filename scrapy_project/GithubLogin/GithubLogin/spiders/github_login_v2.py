# -*- coding: utf-8 -*-
import scrapy
import re


class GithubLoginV2Spider(scrapy.Spider):
    name = 'github_login_v2'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "login":"htwoo111",
                "password":"xxx"
                    },
            callback=self.after_login
        )

    def after_login(self, response):
        print('in after login function')
        name = re.findall(r'htwoo', response.body.decode())
        print(name)