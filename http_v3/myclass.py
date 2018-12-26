#! /usr/bin/python
# coding:utf8
#
import mylib

class HttpHeaderParse(object):
    def __init__(self, data):
	self.data = data

    def get_filename(self, record):
	detail_string = record[5]
	detail_array = detail_string.split(" ")
	return detail_array[1]

    def get_user_ip(self, record):
	return record[1]

    def get_server_ip(self, record):
	return record[1]

    def get_request_time(self, record):
	return record[0]

    def get_response_time(self, record):
	return record[0]

    def get_latence(self, time_request, time_response):
	return mylib.get_latence_microseconds(time_request, time_response)
	
    def get_method(self, record):
	detail_string = record[5]
	detail_array = detail_string.split(" ")
	return detail_array[0]

    def get_status(self, record):
	detail_string = record[5]
	detail_array = detail_string.split(" ")
	return detail_array[1]

    def gen_pretty_item(self, request_method, request_record):
	response_record = ()
	request_ack = request_record[4]
	for row in self.data:
	    response_seq = row[3]
	    if response_seq == request_ack:
		response_record = row
		break;
	if response_record == ():
	    print "没有找到response包"
	    return ()
	# print request_record
	# print response_record
	FIELD_FILENAME = self.get_filename(request_record)
	FIELD_USER_IP = self.get_user_ip(request_record)
	FILED_SERVER_IP = self.get_server_ip(response_record)
	FIELD_REQUEST_TIME = self.get_request_time(request_record)
	FIELD_RESPONSE_TIME = self.get_response_time(response_record)
	FIELD_LATENCE = self.get_latence(FIELD_REQUEST_TIME, FIELD_RESPONSE_TIME)
	FIELD_METHOD = self.get_method(request_record)
	FIELD_STATUS = self.get_status(response_record)
	# print (FIELD_FILENAME, FIELD_USER_IP, FILED_SERVER_IP, FIELD_REQUEST_TIME, FIELD_RESPONSE_TIME, FIELD_LATENCE, FIELD_METHOD, FIELD_STATUS)
	return (FIELD_FILENAME, FIELD_USER_IP, FILED_SERVER_IP, FIELD_REQUEST_TIME, FIELD_RESPONSE_TIME, FIELD_LATENCE, FIELD_METHOD, FIELD_STATUS)

    def parse(self, method):
	item_list = []
	for row in self.data:
	    httpdetail = row[5]
	    if method in httpdetail:
		item = self.gen_pretty_item(method, row)
		item_list.append(item)
	    else:
		pass
	# print item_list
	return item_list


class DataPool(object):
    def __init__(self, conn):
	self.conn = conn

    def fetch_data(self, table):
	cursor = self.conn.cursor()
	try:
	    sql = "SELECT * FROM %s" % table
	    cursor.execute(sql)
	    result = cursor.fetchall()
	    if len(result) < 1:
		raise Exception("数据库 %s 中没有记录" % table)
	except Exception as e:
	    raise Exception("读取数据库失败: " + str(e))
	else:
	    return result
	finally:
	    cursor.close()

    def format_data(self, data):
	httpinfo = HttpHeaderParse(data)
	try:
	    list_parsed = httpinfo.parse('GET')
	    if len(list_parsed) < 1:
		raise Exception("解析成功的数据库记录条数为0")
	except Exception as e:
	    raise Exception("解析数据失败: " + str(e))
	else:
	    return list_parsed

    def insert_data(self, table, data):
	# print data
	for record in data:
	    cursor = self.conn.cursor()
	    try:
		sql = "INSERT INTO %s (filename, userip, serverip, requesttime, responsetime, latence, method, status)" % table
		sql = sql + " values (%s, %s,%s, %s, %s, %s, %s, %s)"
		cursor.execute(sql, record)
	    	if cursor.rowcount != 1:
	    	    raise Exception("插入数据库失败: %s" % sql)
	    except Exception as e:
		# raise e
		raise Exception("插入数据库失败: " + str(e))
	    finally:
	        cursor.close()

    def process1(self, tb_source, tb_target):
	try:
	    data_raw = self.fetch_data(tb_source)
            data_pretty = self.format_data(data_raw)
            self.insert_data(tb_target, data_pretty)
	    self.conn.commit()
	except Exception as e:
	    self.conn.rollback()
	    raise e
