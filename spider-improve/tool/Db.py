# -*- coding:utf-8 -*-

import pymysql.cursors
import os
import sys
sys.path.append('..')
import config.DbConfig as config
import logging

con = None

class Db(object):
    def __init__(self):
        self.__con = self.__getConn()

    def __getConn(self):
        global con
        if not con:
            print 'new connection'
            logging.info('new connection')
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='zuston',
                                         db='spider',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            con = connection
            return connection
        else:
            print 'reuse the connection'
            return con

    def getOne(self):
        try:
            with self.__con.cursor() as cursor:
                sql = "select * from queue limit 10"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
        finally:
            self.__con.close()



if __name__ == '__main__':
    a = Db()
    a.getOne()

