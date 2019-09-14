import requests
import json
import time


class DoubanSpider(object):
    def __init__(self):
        self.all_url = [
            {"url_temp": "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start={}",
             "country": "US"},
            {"url_temp": "https://movie.douban.com/j/search_subjects?type=tv&tag=%E8%8B%B1%E5%89%A7&sort=recommend&page_limit=20&page_start={}",
             "country": "UK"},
            {"url_temp": "https://movie.douban.com/j/search_subjects?type=tv&tag=%E5%9B%BD%E4%BA%A7%E5%89%A7&sort=recommend&page_limit=20&page_start={}",
             "country": "CN"}
        ]
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Cookie": """bid=ritQLC6fjYo; gr_user_id=5918bd21-276d-4a80-9317-718689a1c95f; _vwo_uuid_v2=D9951E2C970B5B64B03F085111A475421|7a828f1c007f53618de9a6fbe511ea9b; __gads=ID=c0940d8498c73862:T=1566175932:S=ALNI_Mak2fzg33Gm17z5mOKN0-1DfstUIw; viewed="10546125_20432061"; ll="118297"; acw_tc=2760826215683820047082070ecbeb1d7604f8a889a38f76339bda1de33afb; __yadk_uid=SDytN8vqYzyGtITpzUOqBCuk97bpwjbV; _ga=GA1.2.930570486.1566136452; _gid=GA1.2.955509093.1568382446; UM_distinctid=16d2ae1bc7768-0a34bf851b571d-5373e62-151800-16d2ae1bc7836b; __utmc=30149280; __utmc=223695111; Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1568382500,1568420406; Hm_lpvt_19fc7b106453f97b6a84d64302f21a04=1568420406; __utma=30149280.930570486.1566136452.1568420138.1568435373.8; __utmz=30149280.1568435373.8.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1568435382%2C%22https%3A%2F%2Fwww.douban.com%2Fgroup%2Fexplore%22%5D; __utma=223695111.7046039.1568382026.1568420033.1568435382.3; __utmz=223695111.1568435382.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/group/explore; trc_cookie_storage=taboola%2520global%253Auser-id%3Db3a7e5e2-901c-4551-b2e2-f87223de51cd-tuct42565a6; _pk_id.100001.4cf6=94cac669206cab03.1568382026.3.1568436141.1568420253."""
        }
        self.proxies = {"https": "https:61.128.208.94:3128"}

    def parse_url(self, url):
        """发送请求，获取数据"""
        print(url)
        r = requests.get(url, headers=self.headers, proxies=self.proxies)
        return r.content.decode()

    def get_content_list(self, json_str):
        dict_ret = json.loads(json_str)
        content_list = dict_ret["subjects"]
        return content_list

    def save_content_list(self, content_list, country):
        with open("../crawl_file/013.douban_spider.txt", "a", encoding="utf-8") as f:
            for content in content_list:
                content["country"] = country
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")  # 追加换行符
            print("保存成功")

    def run(self):
        """实现主程序"""
        # 1.start_url
        for url_dict in self.all_url:
            current_page = 0
            while True:
                url = url_dict["url_temp"].format(current_page)

                # 2.发送请求，获取数据
                json_str = self.parse_url(url)

                # 3.提取数据
                content_list = self.get_content_list(json_str)
                # print(content_list)
                # 4.保存
                self.save_content_list(content_list, url_dict["country"])
                # 设置退出条件
                if (len(content_list) < 20) or (current_page >= 1000):
                    break
                # 5.构造下一个url地址，进入循环
                current_page += 20


if __name__ == "__main__":
    douban_spider = DoubanSpider()
    douban_spider.run()
