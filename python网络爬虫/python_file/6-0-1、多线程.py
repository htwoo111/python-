import threading


def thread_job():
    print("this is an added Thread, number is {}".format(threading.current_thread()))


def main():
    t = threading.Thread(target=thread_job, name="subThread1")
    t.start()
    print(threading.current_thread())
    print("当前活跃的线程数有：{}".format(threading.active_count()))
    # print(threading.enumerate())

if __name__ == "__main__":
    main()