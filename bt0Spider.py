import sys
import time
import os
from multiprocessing import Pool
from bs4 import BeautifulSoup
import redis
from pyTool.tool.Http import *

redisConn = redis.StrictRedis(host='127.0.0.1', port=6379)

def getData(movieUrl):
    start = time.time()
    http = Http()
    [code,msg,res] = http.open(movieUrl)
    # time.sleep(1)
    print 'the process pid is:%s,cost time is:%.2f' % (os.getpid(),time.time()-start)


if __name__ == '__main__':

    print 'parent process is %s' % os.getpid()
    while(True):
        processPool = Pool(5)
        for i in range(4):
            movieNumber = redisConn.spop('movie-url')
            movieUrl = 'http://bt0.com/film_' + str(movieNumber) + '.html'
            processPool.apply_async(getData,args=(movieUrl,))

        processPool.close()
        processPool.join()
        print 'all the process end!'
        break
