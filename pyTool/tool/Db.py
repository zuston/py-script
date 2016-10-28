# -*- coding:utf-8 -*-

import pymysql.cursors
import os
import sys
import pyTool.config.DbConfig as config
import logging

con = None

'''
提供mysql数据库的基础工具类
'''
class Db(object):
    def __init__(self,dbname=None):
        self.__con = self.__getConn()
        self.dbname = dbname if dbname!=None else config.dbname

    def __getConn(self):
        global con
        if not con:
            print 'new connection'
            logging.info('new connection')
            connection = pymysql.connect(host=config.host,
                                         user=config.user,
                                         password=config.password,
                                         db=config.dbname,
                                         charset=config.charset,
                                         cursorclass=pymysql.cursors.DictCursor)
            con = connection
            return connection
        else:
            print 'reuse the connection'
            return con


    def getOne(self,tableName,whereCondition):
        try:
            with self.__con.cursor() as cursor:
                sql = 'select * from '+tableName+' '+whereCondition
                cursor.execute(sql)
                result = cursor.fetchone()
        finally:
            self.__con.close()
            return result

    def insert(self,sql):
        cursor = self.__con.cursor()
        res = cursor.execute(sql)
        pass




if __name__ == '__main__':
    a = Db()
    a.getOne()
