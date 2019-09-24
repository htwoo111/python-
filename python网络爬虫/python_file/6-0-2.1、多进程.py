import multiprocessing as mp
import time


def job(a, b):
    time.sleep(2)
    print("a + b = {}".format(a+b))
    return a+b


def main():
    p1 = mp.Process(target=job, args=(1, 2))
    p1.daemon = True  # 设置守护进程为True，即主进程结束子进程也结束
    p1.start()
    p1.join()


if __name__ == "__main__":
    main()
