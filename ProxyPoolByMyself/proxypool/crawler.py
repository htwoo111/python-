import re
import requests
from requests.exceptions import ConnectionError
from proxypool.parse_url import get_page
import time


class CrawlerMeta(type):
    """
    使用元继承创建Crawler类，
    添加爬虫函数列表和爬虫函数个数
    __CrawlerCount__:爬虫个数
    __CrawlerFunc__：爬虫函数列表
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlerFunc__'] = []
        print('*'*50)
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlerFunc__'].append(k)
                count += 1 
        attrs['__CrawlerCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=CrawlerMeta):
    def get_proxies(self, callback):
        # proxies = []
        # 执行对应网站爬虫
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理：{}'.format(proxy))
            # proxies.append(proxy)
            # return proxies
            yield proxy

    def crawl_xicidaili(self):
        print('开始获取西祠代理')
        for i in range(8, 10):
            # 构造代理url
            url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "www.xicidaili.com",
                "Referer": "https://www.xicidaili.com/nn/2",
                "Upgrade-Insecure-Requests": "1",
            }
            html = get_page(url, options=headers)
            time.sleep(2)
            if html:
                # 寻找trs：所有ip：port包含在tr里面
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                find_port = re.compile('<td>(\d+)</td>')
                trs = find_trs.findall(html)
                for tr in trs:
                    re_ip_address = find_ip.findall(tr)
                    re_port = find_port.findall(tr)
                    # zip（x, y） 递归将两个同样长度的列表（或者其他）一一对应返回一个元组生成器
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ":" + port
                        yield address_port.replace(' ', '')
