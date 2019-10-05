# -*- coding: utf-8 -*-
import scrapy
import re

class GithubLoginSpider(scrapy.Spider):
    name = 'github_login'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        token = response.xpath('//div//input[2]/@value').extract_first()
        # print('token is {}'.format(token))
        post_data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": token,
            "login": "1405360652@qq.com",
            "password": "a201741501113",
            "webauthn-support": "supported",
            "webauthn-iuvpaa-support": "unsupported"
        }

        yield scrapy.FormRequest(
            'https://github.com/session',
            formdata=post_data,
            callback=self.after_login
        )


    def after_login(self, response):
        print('in after login function')
        name = re.findall(r'htwoo', response.body.decode())
        print(name)