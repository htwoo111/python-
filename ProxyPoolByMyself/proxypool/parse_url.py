import requests
from requests.exceptions import ConnectionError

base_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

def get_page(url, options={}):
    """
    爬去代理
    url：目标网站
    options：选项，如headers，proxy
    return：网页源码或者None
    """

    headers = dict(base_headers, **options)
    print('正在爬去url：{}'.format(url))
    try:
        response = requests.get(url, headers=headers)
        print("抓取成功，url：{}， status：{}".format(url, response.status_code))
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('爬取失败：{}'.format(url))
        return None