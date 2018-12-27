#! /usr/bin/python
# coding:utf8
#
import MySQLdb
from myclass import HeatMain


# 1.endpoint信息
endpoint_1 = r'http://10.30.31.121/heat_log/2018-12-01_000-cluster_nodes.log'
endpoint_2 = r'http://10.30.31.121/heat_log/2018-04-03_0000-cluster_nodes.log'

# 2.数据库信息
DB_USER = "root"
DB_HOST = "10.30.30.121"
DB_PASSWORD = ""
DB_DBNAME = "test"
try:
    conn = MySQLdb.Connect(host=DB_HOST, user=DB_USER, db=DB_DBNAME)
except Exception as e:
    print "连接数据库失败: " + str(e)
    exit()

# 3.开始
try:
    heat = HeatMain(conn, endpoint_1)
    heat.fetch_log()
    # print len(heat.logs)	
    heat.parse_log()
    # print len(heat.recordss)
    raw_input("解析数据完毕，确认写入数据库(Ctrl-C退出):")
    heat.store_log()
except Exception as e:
    print "运行失败: " + str(e)
else:
    print "运行成功"
finally:
    heat.statistics()
    conn.close()

