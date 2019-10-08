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

    def crawl_iphai(self):
        print('开始获取iphai代理...')
        # 构造url
        url = 'http://www.iphai.com/'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.iphai.com",
            "Upgrade-Insecure-Requests": "1"
        }
        html = get_page(url, options=headers)
        if html:
            find_ip_port = re.compile(
                '<td>\s*(.*?)\s*</td>\s*<td>\s*(\d+)\s*</td>')
            ip_port_list = find_ip_port.findall(html)
            for ip, port in ip_port_list:
                ip_port = ip + ":" + port
                yield ip_port.replace(' ', '')

    def crawl_66ip(self, start=1, end=3):
        print('开始获取66ip代理...')
        for i in range(start, end):
            # 构造url
            url = 'http://www.66ip.cn/{}.html'.format(i)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.ip3366.net",
                "Referer": "http://www.ip3366.net/free/?stype=1&page=2",
                "Upgrade-Insecure-Requests": "1"
            }
            html = get_page(url, options=headers)
            time.sleep(2)
            if html:
                find_ip_port = re.compile('<tr><td>(.*?)</td><td>(\d+)</td>')
                ip_port_list = find_ip_port.findall(html)
                for ip, port in ip_port_list:
                    ip_port = ip + ":" + port
                    yield ip_port.replace(' ', '')

    def crawl_ip3366(self, start=1, end=3):
        print('开始获取ip3366代理...')
        for i in range(start, end):
            # 构造url
            url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(i)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.ip3366.net",
                "Referer": "http://www.ip3366.net/free/?stype=1&page=2",
                "Upgrade-Insecure-Requests": "1"
            }
            html = get_page(url, options=headers)
            time.sleep(2)
            if html:
                find_ip_port = re.compile(
                    '<tr>\s*<td>(.*?)</td>\s*<td>(\d+)</td>')
                ip_port_list = find_ip_port.findall(html)
                for ip, port in ip_port_list:
                    ip_port = ip + ":" + port
                    yield ip_port.replace(' ', '')

    def crawl_xicidaili(self, start=1, end=3):
        print('开始获取西刺代理...')
        for i in range(start, end):
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
            time.sleep(2)  # 设置间隔时间避免被反爬
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
