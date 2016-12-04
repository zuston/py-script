# --*-- coding:utf-8 --*--
import os
import sys
import time
import random
import multiprocessing


def putQueue(q):
    for value in range(5):
        print "放入队列中:",value
        q.put(value)
        time.sleep(random.random())

def getQueue(q):
    while 1:
        print "获取的数值:",q.get()


if __name__ == '__main__':
    q = multiprocessing.Queue()
    pw = multiprocessing.Process(target=putQueue,args=(q,))
    pr = multiprocessing.Process(target=getQueue,args=(q,))

    pw.start()
    pr.start()

    pw.join()
    pr.terminate()