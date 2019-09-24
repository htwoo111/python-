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
    ret = 1
    for i in range(10000):
        ret += i + i**2 + i**3

    q.put(ret)

@decorator
def main():
    q = mp.Queue()
    ps = []
    for i in range(2):
        p = mp.Process(target=job1, args=(q,))
        p.start()
        ps.append(p)
    for p in ps:
        p.join()
    ret1 = q.get()
    ret2 = q.get()
    print(ret1, "  ", ret1+ret2)
# def job2()

if __name__ == "__main__":
    main()
    print('main done')
