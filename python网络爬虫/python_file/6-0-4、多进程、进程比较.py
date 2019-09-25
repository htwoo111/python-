import multiprocessing as mp
import threading as td
import time


def decorator(func):
    def wrap(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print("{} spend time : {:.8f}".format(func.__name__, end-start))
        return ret
    return wrap


def process():
    ret = 1
    for i in range(100000):
        ret = i + i**2 + i**3
    print('Process done :', ret)


@decorator
def normal():
    for n in range(4):
        ret = 1
        for i in range(100000):
            ret = i + i**2 + i**3
        print('normal done :', ret)


@decorator
def main_p():
    ps = []
    for i in range(4):
        p2 = mp.Process(target=process)
        # p2.daemon = True
        p2.start()
        ps.append(p2)
    for p in ps:
        p.join()


@decorator
def thread():
    ts = []
    for i in range(4):
        t = td.Thread(target=process)
        # t.daemon = True
        t.start()
        ts.append(t)
    for t in ts:
        t.join()


if __name__ == "__main__":
    main_p()
    normal()
    thread()
