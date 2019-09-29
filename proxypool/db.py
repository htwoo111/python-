import redis 
from random import choice
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITAL_SCORE
import re


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
            """
            初始化
            :param host: Redis 地址
            :param port: Redis 端口
            :param password: Redis密码
            """
            self.db = redis.StrictRedis(host=host, port=port, password=password, decode_response=True)

    def add(self, )