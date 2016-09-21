import os,sys
import Queue
from multiprocessing.managers import BaseManager
import random


if __name__ == '__main__':

    class QueueManager(BaseManager):
        pass

    taskQueue = Queue.Queue()
    resQueue = Queue.Queue()

    QueueManager.register('get_task',callable=lambda :taskQueue)
    QueueManager.register('get_res',callable=lambda :resQueue)

    manager = QueueManager(address=('',6000),authkey='zuston')
    manager.start()

    task = manager.get_task()
    res = manager.get_res()


    for value in range(5):
        i = random.randint(0,1000)
        task.put(i)
        print 'master put ',i

    print ''
    print 'trying get the res'
    for i in range(5):
        r = res.get()
        print 'client get ',r

    manager.shutdown()