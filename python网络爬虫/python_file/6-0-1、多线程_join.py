import threading
import time


def thread_job():
    print('T1 start {}\n'.format(threading.current_thread()))
    for i in range(10):
        time.sleep(0.1)
    print('T1 end {}\n'.format(threading.current_thread()))


def main():
    t1 = threading.Thread(target=thread_job, name="t1")
    t1.start()
    # 子线程不用join()，主线程会继续执行自己的任务，
    # 执行结束后等待子线程执行结束，程序才算结束
    t1.join()
    print('main thread end {}\n'.format(threading.current_thread()))


if __name__ == "__main__":
    main()
