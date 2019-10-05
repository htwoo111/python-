# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random

class RandomUserAgentMiddleware:
    
    def process_request(self, request, spider):
        USER_AGENT = random.choice(spider.settings.get('USER_AGENT_LIST'))
        request.headers['User_Agent'] = USER_AGENT


class CheckUserAgent:

    def process_response(self, request, response, spider):
        # print(dir(response.request))
        print(request.headers['User_Agent'])
        return response