from random import choice
import redis
import re
from proxypool.error import PoolEmptyError
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'htwoo111'
# REDIS_KEY = 'myProxies'
REDIS_KEY = 'test'


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        host：地址
        post：端口号
        password：密码
        """
        self.db = redis.StrictRedis(
            host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理
        proxy：代理
        score：代理的分数
        return：返回添加结果
        """
        if not re.mathch('\d+\.\d+\.\d+\.\d+:\d+', proxy):
            print('代理：{}不符合规范，丢弃'.format(proxy))
        if not self.exists:
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def exists(self, proxy):
        """
        判断代理是否存在
        proxy：代理
        return：是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def random(self):
        """
        随即获取代理，先从获取分数最高的代理，如果不存在，则按照排名获取
        return：随即代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        扣分，如果代理分数小于最小值则删除
        proxy：代理
        return：修改后的分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print("代理：{}当前分数为{}, 减1".format(proxy, score))
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理：{} 当前分数为{}, 移除'.format(proxy, score))
            return self.db.zrem(REDIS_KEY, proxy)

    def max(self, proxy):
        """将代理分数设置为MAX_SCORE
        proxy:代理
        return：设置的结果
        """
        print('代理:{}可用， 设置为最高分：{}'.format(proxy, MAX_SCORE))
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        return：代理的数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        return：全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        start：开始的索引
        stop：结束的索引
        return：搜索的代理的列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop-1)


if __name__ == "__main__":
    conn = RedisClient()
    result = conn.batch(1, 5)
    print(result)