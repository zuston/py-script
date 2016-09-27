import redis as rd
import os
import sys
sys.path.append('..')
import config.DbConfig as config

class ZRedis(object):
    def __init__(self):
        self._instanceRedisConn()

    def _instanceRedisConn(self):
        self.redisConn = rd.StrictRedis(host=config.redisDict['host'], port=config.redisDict['port'])


if __name__ == '__main__':
    redis = ZRedis()
    print redis.redisConn.sadd('hello',3)
