import requests
import json
import os

WC_MASK_IMG = './images/wawa.jpg'

class JDSpider(object):
    def __init__(self):
        self.url_temp = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6983&productId=1263013576&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Referer": "https://item.jd.com/1263013576.html"
        }
        self.proxies = {"https": "https:61.128.208.94:3128"}
        self.COMMENT_FILE_PATH = "./000.test.txt"

    def parse_url(self, url):
        """发送请求，获取数据"""
        print(url)
        try:
            r = requests.get(url, headers=self.headers, proxies=self.proxies)
            r.raise_for_status()
            json_str = r.text[26:-2]
            print(r.encoding)
            return json_str
        except:
            print("爬取失败")
        # 截取json数据字符串

    def get_content_list(self, json_str):
        dict_ret = json.loads(json_str)
        content_list = dict_ret["comments"]
        return content_list

    def save_data(self, content_list):
        # if os.path.exists(self.COMMENT_FILE_PATH):
            # os.remove(self.COMMENT_FILE_PATH)
        with open(self.COMMENT_FILE_PATH, "a", encoding="utf-8") as f:
            for content in content_list:
                comments = content['content']
                f.write(json.dumps(comments, ensure_ascii=False))
                f.write("\n")  # 打印换行符
        print("保存成功")

    def run(self):
        """
        实现主程序
        :current_page: 爬取的页数，初始化为0
        """
        current_page = 0
        while True:
            # 1.获取url
            url = self.url_temp.format(current_page)
            # 2.发送请求，获取数据
            json_str = self.parse_url(url)
            # 3.提取数据
            content_list = self.get_content_list(json_str)
            # 4.写入数据
            self.save_data(content_list)
            # 5.设置下一个url
            if (len(content_list) < 10) or (current_page == 500):
                break
            current_page += 1


if __name__ == "__main__":
    jd_spider = JDSpider()
    jd_spider.run()

