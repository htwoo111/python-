import re
import json
import requests


class NeiHan(object):
    def __init__(self):
        """
        初始化：
        :self.headers: 请求网页头
        :temp_url: 获取段子的网页
        """
        self.temp_url = "http://www.haha56.net/xiaohua/neihan/index_7_{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Referer": "http://www.haha56.net/xiaohua/neihan/",
            "Cookie": "BAIDU_SSP_lcr=https://www.baidu.com/link?url=ndcdorGj7sYqPoMtaB2t8pSgnaf6A6w0lgbJawXPx6TynfNsN0hJ-5anzl2jsRZG&wd=&eqid=d27c0d9f000c9aae000000065d7d8291; Hm_lvt_9b496e3d6adef11b924b6b261a56dff8=1568506533; BDTUJIAID=22f3ffff35d9844d6b200f1379341a60; Hm_lpvt_9b496e3d6adef11b924b6b261a56dff8=1568507483"
        }


    def send_request(self, url):
        r = requests.get(url, headers=self.headers)
        r.encoding = 'gb2312'
        return r.text

    def get_data(self, html_str):
        ret = re.findall(r'<p>.*?(.*)</p>', html_str, re.S)
        return ret



    def run(self):
        # 1. 获取第一页url
        start_url = self.temp_url.format(1)

        # 2. 发送请求，获取数据
        html_str = self.send_request(start_url)
        # 3. 提取数据
        data = self.get_data(html_str)
        # 4. 保存

        # 5. 构造下一页的数据
        return data


if __name__ == "__main__":
    neihan_spider = NeiHan()
    content = neihan_spider.run()

    print(content)
    print()