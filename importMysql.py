#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import MySQLdb
import pymysql.cursors
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xlrd
book = xlrd.open_workbook("0815patent.xlsx",encoding_override='utf-8')
sh = book.sheet_by_index(0)
print sh.name
print sh.nrows
print sh.ncols
# print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
sql = 'insert into company(cname,cnumber) values'
for rx in range(1,sh.nrows):
    # 获取全部class属性
    # print dir((sh.row(rx))[0])
    # 企业编号
    cid = str(((sh.row(rx))[0].value))
    cid = cid[:-2]
    # print cid
    # 公司名称
    cname = ((sh.row(rx))[1]).value
    # print cname
    sql += "('"+cname+"','"+cid+"'),"
sql = sql[:-1]
sql += ";"
print sql


# db = MySQLdb.connect("localhost","root","shacha","patent",charset='utf8')
# cursor = db.cursor()
# cursor.execute(sql)
# data = cursor.fetchone()
# print int(data[0])
# print data[1]
#
# db.close()

import pymysql.cursors

# Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='zuston',
#                              db='spider',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#
# try:
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "select * from queue limit 1"
#         cursor.execute(sql)
#         result = cursor.fetchone()
#         print(result)
# finally:
#     connection.close()

