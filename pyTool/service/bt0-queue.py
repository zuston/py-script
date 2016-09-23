import sys
import time
import os
sys.path.append("..")
from bs4 import BeautifulSoup
import redis
from tool.Http import *
from multiprocessing.dummy import Pool

redisConn = None
def Ctime(func):
    def wrapper(*args,**kw):
        startTime = time.time()
        res = func(*args,**kw)
        print 'costTime:%.2f'%(time.time()-startTime)
        return res
    return wrapper

def spider(i):
    http = Http()
    global  redisConn
    url = 'http://bt0.com/film-dwonload/1-0-0-0-0-'+str(i)+'.html'
    print url
    [code,msg,res] = http.open(url)

    if code == 200:
        bs = BeautifulSoup(res)
        page = bs.select('.browse-movie-bottom')
        for pg in page:
            movieUrl = pg.a['href'].split('.')[0].split('_')[1]
            movieName = pg.a.string
            movieTime = (pg.select('.browse-movie-year')[0].string).strip()
            print movieName,'--',movieTime
            # if not redisConn.sadd('movie-url',movieUrl):
            #     print 'save error'

if __name__ == '__main__':
    global redisConn
    redisConn = redis.StrictRedis(host='127.0.0.1', port=6379)
    urls = [x for x in range(1,2235)]
    # p1Time = time.time()
    # p = Pool(4)
    # p.map(spider,urls)
    # p.close()
    # p.join()
    # oneTime = time.time()-p1Time
    #
    # p1Time = time.time()
    # p = Pool(5)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    # twoTime = time.time()-p1Time
    #
    # p1Time = time.time()
    # p = Pool(6)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    # threeTime = time.time() - p1Time

    p1Time = time.time()
    p = Pool(7)
    p.map(spider, urls)
    p.close()
    p.join()
    fourTime = time.time() - p1Time

    # p1Time = time.time()
    # p = Pool(8)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    # fiveTime = time.time() - p1Time
    #
    # p1Time = time.time()
    # p = Pool(9)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    # sixTime = time.time() - p1Time


    # p = Pool(7)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    #
    # p = Pool(8)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    #
    # p = Pool(9)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    #
    # p = Pool(10)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    #
    # p = Pool(11)
    # p.map(spider, urls)
    # p.close()
    # p.join()
    #
    # p = Pool(12)
    # p.map(spider, urls)
    # p.close()
    # p.join()

    # print oneTime
    # print twoTime
    # print threeTime
    print fourTime
    # print fiveTime
    # print sixTime





