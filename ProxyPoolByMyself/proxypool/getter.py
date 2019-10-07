from proxypool.redis_db import RedisClient
from proxypool.crawler import Crawler
import sys

POOL_UPPER_THRESHOLD = 200
class Getter(object):
    def __init__(self):
        """
        初始化数据库和创建爬虫
        """
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断代理池是否达到上限
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('或取器开始运作...')
        # 判断代理池是否达到上限
        if not self.is_over_threshold():
            # 遍历所有的代理网站生成的各自的解析函数
            for crawler_index in range(self.crawler.__CrawlerCount__):
                # 获取对应索引的回调函数
                callback = self.crawler.__CrawlerFunc__[crawler_index]
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    # print(proxy)
                    self.redis.add(proxy)