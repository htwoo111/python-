'''
Pool可以提供指定数量的进程，供用户调用，
当有新的请求提交到pool中时，如果池还没有满，
那么就会创建一个新的进程用来执行该请求；
但如果池中的进程数已经达到规定最大值，
那么该请求就会等待，直到池中有进程结束，
才会创建新的进程来它。
'''
from multiprocessing import Lock, Pool
import time


def function(index):
    print("start process ", index)
    time.sleep(3)
    print('end process ', index)


if __name__ == "__main__":
    pool = Pool(processes=3)
    for i in range(4):
        # 非堵塞可以一下子把所有的进程加到进程池里面，而不必等待某一个进程执行结束
        pool.apply(function, (i, ))

    print("start processes...")
    pool.close()
    pool.join()
    print("subprocess done")
