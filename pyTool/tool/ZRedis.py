#!coding:utf-8

import redis
import os



class ZRedis(object):
    def __init__(self):
        redisDict = {'host': '127.0.0.1', 'port': 6379, 'proxyName': 'zproxy'}
        self.redisConn = redis.StrictRedis(host=redisDict['host'], port=redisDict['port'])
        self.containerName = None

    def setContainerName(self,name):
        self.containerName = name

    def push(self,value):
        self.redisConn.lpush(self.containerName,value)

    def pop(self):
        return self.redisConn.lpop(self.containerName)

    def isEmpty(self):
        return self.redisConn.llen(self.containerName)==0

    def len(self):
        return self.redisConn.llen(self.containerName)

    def flush(self):
        self.redisConn.delete(self.containerName)

if __name__ == '__main__':
    zr = ZRedis()
    print zr.pop()
    print zr.redisConn.llen(zr.containerName)