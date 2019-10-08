import asyncio
import aiohttp
import time
import sys
from proxypool.settings import VAILD_STATUS_CODE, TEST_URL, BATCH_TEST_SIZE
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
from proxypool.redis_db import RedisClient

# VAILD_STATUS_CODE = [200]
# TEST_URL = 'https://www.bilibili.com/'
# BATCH_TEST_SIZE = 100
TIME_OUT = 10


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test__single_proxy(self, proxy):
        """
        异步测试单个代理
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(TEST_URL, proxy=real_proxy, timeout=TIME_OUT) as response:
                        if response.status == 200:
                            self.redis.max(proxy)
                            print('代理可用：', proxy)
                        else:
                            self.redis.decrease(proxy)
                            print('代理响应玛不为200： {} , 响应玛：{}'.format(proxy, response.status))
                except (ProxyConnectionError, TimeoutError, ValueError) as e:
                    self.redis.decrease(proxy)
                    print('代理请求失败： ', proxy)
                    print('error is ', e)
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as s:
            self.redis.decrease(proxy)
            print(s)
            pass

        # conn = aiohttp.TCPConnector(verify_ssl=False)
        # async with aiohttp.ClientSession(connector=conn) as session:
        #     try:
        #         if isinstance(proxy, bytes):
        #             proxy = proxy.decode('utf-8')
        #         real_proxy = 'http://' + proxy
        #         print('正在测试', proxy)
        #         async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
        #             if response.status in VALID_STATUS_CODES:
        #                 self.redis.max(proxy)
        #                 print('代理可用', proxy)
        #             else:
        #                 self.redis.decrease(proxy)
        #                 print('请求响应码不合法 ', response.status, 'IP', proxy)
        #     except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
        #         self.redis.decrease(proxy)
        #         print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        """
        print('Tester开始运作...')
        try:
            count = self.redis.count()
            print('当前剩余： {} 个代理'.format(count))
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE, count)
                print('正在测试第 {} - {} 个代理'.format(start+1, stop))
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test__single_proxy(
                    proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
            # logger.debug('测试器发生错误：{}'.format(e.args))
