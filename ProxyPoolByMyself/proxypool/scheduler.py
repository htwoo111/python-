import time
from multiprocessing import Process
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.api import app
from proxypool.settings import GETTER_ENABLED, TESTER_ENABLED,API_ENABLED
from proxypool.settings import GETTER_CYCLE, TESTER_CYCLE
from proxypool.settings import API_HOST, API_PORT
# GETTER_CYCLE = 20
# GETTER_ENABLED = True

# TESTER_CYCLE = 20
# TESTER_ENABLED = True

# API_ENABLED = True
# API_HOST = 'localhost'
# API_PORT = 5555


class Scheduler(object):
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        cycle：从网页获取代理的时间间隔
        """
        getter = Getter()
        while True:
            print('*'*50)
            print('开始抓取代理...')
            print('*'*50)
            getter.run()
            time.sleep(cycle)

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        cycle：从验证代理的时间间隔
        """
        tester = Tester()
        while True:
            print('*'*50)
            print('开始验证代理可用性...')
            print('*'*50)
            tester.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启AIP
        """
        print('*'*50)
        print('开启API...')
        print('*'*50)
        app.run(API_HOST, API_PORT)

    def run(self):
        """
        使用多线程实现代理池运作
        每一个模块使用一个进程
        GETTER_ENABLED：爬取代理模块开关
        """
        print('*'*50)
        print('代理池开始运作...')
        print('*'*50)
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()