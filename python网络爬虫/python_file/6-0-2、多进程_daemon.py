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
        # daemon = True 表明该线程不重要，只要主线程结束，该线程不管有没有执行完代码，都会被关闭
        p.daemon = True  
        p.start()

    print('end...............')  # 主进程之间执行完就关闭所有的程序