import multiprocessing as mp
import time


def decorator(func):
    def wrap(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print("spend time : {:.8f}".format(end-start))
        return ret
    return wrap


def job1(q):
    for i in range(10000):
        ret = i
        q.put(ret)
    print('job1 done')


# def job2(q):
#     for i in range(10000):
#         ret = i
#         q.put(ret)
#     print('job2 done')
def job2(q):
    time.sleep(0.01)
    print('job2 start')
    while not q.empty():
        print("\n{}".format(q.get()))
    print("job2 done")


@decorator
def main():
    q = mp.Queue()  # 使用q队列可以实现进程间通信
    ps = []
    p1 = mp.Process(target=job1, args=(q,))
    ps.append(p1)
    p1.start()
    for i in range(10):
        p2 = mp.Process(target=job2, args=(q,))
        p2.daemon = True
        p2.start()
        ps.append(p2)
    # for p in ps:
        # p.join()
    # p1.join()


if __name__ == "__main__":
    main()
    print('main done')
