import sys
import time
import os
sys.path.append("..")
from bs4 import BeautifulSoup
import redis
from tool.Http import *

http = Http()
redisConn = redis.StrictRedis(host='127.0.0.1', port=6379)

while(True):
    movieNumber = redisConn.spop('movie-url')
    movieUrl = 'http://bt0.com/film_'+str(movieNumber)+'.html'

