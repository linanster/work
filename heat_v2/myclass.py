#! /usr/bin/python
# coding:utf8
#
import urllib2
import json

class HeatLogParser(object):
    def __init__(self):
	pass

    # 参数str_log_json为形如[{"node_ifs_bytes_total": "E"的字符串
    def _parse_json(self, str_log_json):
	op_details_parsed = []
	op_key = ''
	op_rate = ''
	op_path = ''
	# json的最外层是一个列表[]
	# level_1 is a List
	item_level_1 = json.loads(str_log_json)
	if not isinstance(item_level_1, list):
	    return []
	for item_level_2 in item_level_1:
	    # 第二层应该是一个字典{}
	    # level_2 is Dict
	    if not isinstance(item_level_2, dict):
		continue
	    for item_level_3_k, item_level_3_v in item_level_2.items():
		# 第三层每一项是一对k-v，v应该是一个列表[]
		# item_level_3_v is List
		if not isinstance(item_level_3_v, list):
		    continue
		op_key = item_level_3_k.encode('utf-8')
		for item_level_4 in item_level_3_v:
		    # 第四层（即item_level_3_v的下一级）的类型是字典{op_rate:..., path:"...."}
		    # level_4 is Dict
		    if not isinstance(item_level_4, dict):
			continue
		    try:
			# 如果找不到op_rate和op_path，跳过
			if not item_level_4.get('op_rate') or not item_level_4.get('path'):
			    continue
			op_rate = item_level_4['op_rate']
			op_path = item_level_4['path'].encode('utf-8')
		    except Exception as e:
			# 这里有异常，打印异常信息，但并不中断程序。
			print "寻找op_rate和op_path处异常一次: " + str(e)
			continue
		    else:
			op_details_parsed.append((op_key, op_rate, op_path))
	return op_details_parsed




    # 参数logs为(str_time, str_log_json)二元组,返回records为四元组(op_time, op_key, op_rate, op_path)的列表[]
    def parse(self, log):
	records = []
	op_time = log[0]
    	op_details = self._parse_json(log[1])
	for op_detail in op_details:
	    op_key = op_detail[0]
	    op_rate = op_detail[1]
	    op_path = op_detail[2]
            records.append((op_time, op_key, op_rate, op_path))
	return records

class Heat(object):
    def __init__(self, conn, endpoint):
	self.conn = conn
	self.endpoint = endpoint
	self._count_log = 0
	self._count_db = 0
	# logs[]是一个列表，每个列表项是一个二元组(str_time, str_log_json)
	self.logs = []
	# recordss[] 是一个列表l1，每个列表项又是一个列表l2，其中列表l2的每一项是一个四元组(op_time, op_key, op_rate, op_path)
	self.recordss = []
	# 解析器,用于将logs[]中的每一个数据项解析为recordss[]中的每一个数据项
	self.parser = HeatLogParser()


    def statistics(self):
	print "----Statistics----"
	print "共解析出数据 %d 条" % self._count_log
	print "成功插入数据库 %d 条" % self._count_db
	print "------------------"
	    

    def fetch_log(self):
	response = urllib2.urlopen(self.endpoint)
	if response.getcode() != 200:
	    raise Exception("打开 %s 失败" % self.endpoint)
	try:
	    html = response.read()	    		
	    lines = html.split('\n')
	    flag_time = False
	    flag_data = False
	    for line in lines:
		if line.startswith("20"):
		    line_time = line
		    flag_time = True
		elif line.startswith('['):
		    line_data = line
		    flag_data = True
		else:
		    Flag_1 = False
		    Flag_2 = False
		if flag_time and flag_data:
		    # 填写self.logs
		    self.logs.append((line_time, line_data))
		    flag_time = False
		    flag_data = False
	except Exception as e:
	    raise Exception("获取数据(fetch_log)错误: " + str(e))

    def parse_log(self):
	try:
	    for log in self.logs:
		records = self.parser.parse(log)
		# 填写self.recordss
		self.recordss.append(records)
	except Exception as e:
	    raise Exception("解析数据(parse_log)错误: " + str(e))

    def store_log(self):
	# 数据库名(tb_heat)和列名在这里写死了
	sql = "INSERT INTO tb_heat (op_time, op_key, op_rate, op_path) values (%s, %s, %s, %s)"
	try:
	    for records in self.recordss:
		# 以每个时间点对应的日志数据为单位进行提交或回滚
		try:
		    for record in records:
			self._count_log += 1
			try:
			    cursor = self.conn.cursor()
			    cursor.execute(sql, record)
			except Exception as e:
			    raise Exception("插入 %s 错误" % str(record) + str(e))
			else:
			    self._count_db += 1
			finally:
			    cursor.close()
		except Exception as e:
		    self.conn.rollback()
		    raise e
		else:
		    # raw_input("提交确认：")
		    self.conn.commit()
	except Exception as e:
	    raise Exception("存储数据(store_log)错误: " + str(e))
