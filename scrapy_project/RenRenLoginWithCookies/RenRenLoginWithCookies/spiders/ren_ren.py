# -*- coding: utf-8 -*-
import scrapy
import re

class RenRenSpider(scrapy.Spider):
    name = 'ren_ren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/972226806/profile']

    def start_requests(self):
        cookies = 'anonymid=k0g46ao4-9in165; _r01_=1; jebe_key=a52705ae-563c-4962-a999-0807785652ba%7Cad014a7ef6dfe9bf44949cd561542883%7C1568258017513%7C1%7C1568258017627; ln_uact=15622971239; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; _de=F93652EAFE0EF51A2B0DF8B67AF8DF30; springskin=set; depovince=ZGQT; jebecookies=d10d434e-502b-4d2f-b7b6-ed6ab12c8a23|||||; JSESSIONID=abciwR6lZqh4Len6ZBA2w; ick_login=be0d0be8-9486-4269-9eff-eaef28fe935f; p=7a15cfe01e3786f88022f538d594e6fb6; first_login_flag=1; t=d892dc50ff7864f0c536c6007450183a6; societyguester=d892dc50ff7864f0c536c6007450183a6; id=972226806; xnsid=6590a966; ver=7.0; loginfrom=null; wp_fold=0; jebe_key=a52705ae-563c-4962-a999-0807785652ba%7Cad014a7ef6dfe9bf44949cd561542883%7C1568258017513%7C1%7C1570255173945'
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split('; ')}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )
        

    def parse(self, response):
        # name = response.xpath('//').re(r'李明')
        print(response.status)
        # with open('ren_ren.html', 'w', encoding='utf-8') as f:
            # f.write(response.body.decode('utf-8'))
        name = re.findall(r'李明', response.body.decode('utf-8'))
        print(name)
        yield scrapy.Request(
            'http://www.renren.com/972226806',
            callback=self.parse_detail,
        )

    def parse_detail(self, response):
        # name = re.findall(r'李明', response.body.decode('utf-8'))
        name = response.xpath('.').re(r'李明')
        print('parse detail')
        print(name)