from multiprocessing import Process
import time

class MyProcess(Process):
    def __init__(self, loop, *args, **kwargs):  
        super().__init__(*args, **kwargs) # 重写父类方法
        self.loop = loop
        
    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print("PID: {} LoopCount: {}".format(self.pid, count))
            
if __name__ == "__main__":
    for i in range(2,5):
        p = MyProcess(i)
        p.start()

    print('end...............')  # 主进程会先执行完，等待子进程执行结束
        