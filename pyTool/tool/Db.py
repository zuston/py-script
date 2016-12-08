# -*- coding:utf-8 -*-

import pymysql.cursors
import os
import sys
import logging

con = None

'''
提供mysql数据库的基础工具类
'''
class Db(object):
    def __init__(self,dbname=None):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'shacha',
            'dbname': 'todo',
            'charset': 'utf8mb4',
        }
        self.dbname = dbname if dbname!=None else self.config['dbname']
        self.__con = self.__getConn()


    def __getConn(self):
        global con
        if not con:
            print 'new connection'
            logging.info('new connection')
            connection = pymysql.connect(host=self.config['host'],
                                         user=self.config['user'],
                                         password=self.config['password'],
                                         db=self.dbname,
                                         charset=self.config['charset'],
                                         cursorclass=pymysql.cursors.DictCursor)
            con = connection
            return connection
        else:
            print 'reuse the connection'
            return con


    def getOne(self,tableName,whereCondition=None):
        if whereCondition is None:
            whereCondition = ''
        result = None
        try:
            with self.__con.cursor() as cursor:
                sql = 'select * from '+tableName+' '+whereCondition
                # sql = tableName
                cursor.execute(sql)
                result = cursor.fetchone()
        finally:
            # self.__con.close()
            return result

    def insert(self,sql):
        result = 0
        try:
            with self.__con.cursor() as cursor:
                result = cursor.execute(sql)
        finally:
            # self.__con.close()
            return result

    def execute(self,sql):
        result = None
        try:
            with self.__con.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            # self.__con.close()
            return result



if __name__ == '__main__':
    a = Db()
    result = a.execute("select * from thing")
    print result