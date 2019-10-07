import time
from multiprocessing import Process
from proxypool.getter import Getter

GETTER_CYCLE = 20
GETTER_ENABLED = True


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
