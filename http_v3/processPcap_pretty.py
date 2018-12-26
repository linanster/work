#! /usr/bin/python
# coding:utf8
#
import MySQLdb
import time
import mylib
import myclass

# Database info
DB_USER = "root"
DB_HOST = "10.30.30.121"
DB_PASSWORD = ""
DB_DBNAME = "test"

# Table info
TB_RAW = 'data_pcap_raw'
TB_PRETTY = 'data_pcap_pretty'

try:
    conn = MySQLdb.Connect(host=DB_HOST, user=DB_USER, db=DB_DBNAME)
except Exception as e:
    print "连接数据库失败: " + str(e)
    exit()

try:
    httpdata = myclass.DataPool(conn)
    httpdata.process1(TB_RAW,TB_PRETTY)
    print "运行成功"
except Exception as e:
    print "运行失败: "+str(e)
finally:
    conn.close()

