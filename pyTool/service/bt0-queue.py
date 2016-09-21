import sys
import time
import os
sys.path.append("..")
from bs4 import BeautifulSoup
import redis
from tool.Http import *

http = Http()
redisConn = redis.StrictRedis(host='127.0.0.1', port=6379)
for i in range(1,2235):
    url = 'http://bt0.com/film-dwonload/1-0-0-0-0-'+str(i)+'.html'
    print url
    [code,msg,res] = http.open(url)

    if code == 200:
        bs = BeautifulSoup(res,'lxml')
        page = bs.select('.browse-movie-bottom')
        for pg in page:
            movieUrl = pg.a['href'].split('.')[0].split('_')[1]
            movieName = pg.a.string
            movieTime = (pg.select('.browse-movie-year')[0].string).strip()
            print movieName,'--',movieTime
            if not redisConn.sadd('movie-url',movieUrl):
               print 'save error'

