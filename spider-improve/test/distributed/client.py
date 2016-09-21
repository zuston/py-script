import time, sys, Queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

QueueManager.register('get_task')
QueueManager.register('get_res')

server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)
m = QueueManager(address=(server_addr, 6000), authkey='zuston')
m.connect()
task = m.get_task()
result = m.get_res()
for i in range(5):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty.')
print('worker exit.')
