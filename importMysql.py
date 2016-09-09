#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xlrd
book = xlrd.open_workbook("0815patent.xlsx",encoding_override='utf-8')
# print("The number of worksheets is {0}".format(book.nsheets))
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
    # print cid
    # 公司名称
    cname = ((sh.row(rx))[1]).value
    # print cname
    sql += "('"+cname+"','"+cid+"'),"
sql = sql[:-1]
print sql
db = MySQLdb.connect("localhost","root","shacha","patent",charset='utf8')
cursor = db.cursor()
cursor.execute(sql)
# data = cursor.fetchone()
# print int(data[0])
# print data[1]
#
db.close()

