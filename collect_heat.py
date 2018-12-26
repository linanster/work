import requests    
import pymysql 
import json
import time




while(1):
    url = "https://10.224.36.48:8080/platform/1/statistics/current?keys=node.ifs.heat&substr=true&degraded=true"  
    r = requests.get(url,auth=('root', 'a'),verify=False)
    #print(r.json()['stats'][0]['devid'])
    for item in r.json()['stats']:
      #print("\n")
      #print(isinstance(item['value'],list))
      #print(isinstance(item['value'],dict))
      #print(isinstance(item['value'],float))
      #print("\n")
      
      if isinstance(item['value'],list):
          for pa in item['value']:
              print("\n")
              print(item['key'])
              print(str(pa['op_rate']))
              print(pa['path'])
              print(item['time'])
              print("\n")
              db = pymysql.connect(host='localhost',user='root',password='root',db='sys',port=3306)
              cursor = db.cursor()
              sql_insert = """insert into isilon (op_key,op_time,op_rate,path) values()"""
              try:    
                cursor.execute("""insert into isilon (op_key,op_time,op_rate,path) values(%s,%s,%s,%s)""",(item['key'],item['time'],pa['op_rate'],pa['path']))    
    #提交事务   
                db.commit()    
                print("insert ok")
              except Exception as e:    
    #如果异常则回滚事务    
                db.rollback()    
                raise e #可做自己想做的事
              finally:   
                db.close()
                
      if isinstance(item['value'],dict):
          for pa in item['value']['lins']:
              print("\n")
              print(item['key'])
              print(str(pa['op_rate']))
              print(pa['lin'])
              print(item['time'])
              print("\n")
              db = pymysql.connect(host='localhost',user='root',password='root',db='sys',port=3306)
              cursor = db.cursor()
              sql_insert = """insert into isilon (op_key,op_time,op_rate,path) values()"""
              try:    
                cursor.execute("""insert into isilon (op_key,op_time,op_rate,lin) values(%s,%s,%s,%s)""",(item['key'],item['time'],pa['op_rate'],pa['lin']))    
    #提交事务   
                db.commit()    
                print("insert ok")
              except Exception as e:    
    #如果异常则回滚事务    
                db.rollback()    
                raise e #可做自己想做的事
              finally:   
                db.close()
    time.sleep(600)