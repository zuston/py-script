import os
import sys
import redis
sys.path.append('..')
import config.DbConfig as config

class ZProxy(object):
    def __init__(self):
        self.proxyName = config.redisDict['proxyName']
        self._getRedisConn()

    def _getRedisConn(self):
        self.redisConn = redis.StrictRedis(host=config.redisDict['host'],port=config.redisDict['port'])

    def _getProxyIp2Pool(self):
        pass


    def getLastedIp(self):
        count = self.redisConn.zcard(self.proxyName)
        if count <= 1 or count is None:
            self._getProxyIp2Pool()
            return getLastedIp()
        else:
            proxyIP = self.redisConn.spop(self.proxyName)
            return proxyIP

    def getRandomIp(self):
        pass

    def flushPool(self):
        pass

    def test(self):
        print self.redisConn.get('hello')




if __name__ == '__main__':
    proxy = ZProxy()
    print proxy.test()
