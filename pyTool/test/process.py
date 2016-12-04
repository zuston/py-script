#! coding:utf-8

import os
from threading import Thread
import threading
import time
import multiprocessing

exitFlag = False
count = 0
lock = threading.Lock()
def task(name,n):
    for i in range(n):
        global count
        global lock
        if exitFlag is not True:
            print name+":"+str(i)
            lock.acquire()
            count += 1
            lock.release()
            time.sleep(1)
        else:
            break


# 多进程变量无法同步,需要使用主进程队列来进行同步
pp = 0
def multiProcessTask():
    for i in range(5):
        global pp
        pp += 1
        print "pp:"+str(pp)

if __name__ == '__main__':
    t1 = Thread(target=task,args=("t1",4))
    t1.start()
    t2 = Thread(target=task,args=('t2',8))
    t2.start()
    while t2.is_alive():
        if not t1.is_alive():
            exitFlag = True
    print 'main finish'
    print count

    mt1 = multiprocessing.Process(target=multiProcessTask)
    mt2 = multiprocessing.Process(target=multiProcessTask)
    mt1.start()
    mt2.start()

    print "pp:"+str(pp)
