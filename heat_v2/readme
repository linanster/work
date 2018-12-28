1.myclass.py
自定义类文件
-- HeatMax
-- HeatMain

2.main_min.py
(1) 解析一个endpoint，并写入数据库
(2) 主类为HeatMain
    -- 接收两个参数：endpoint和conn
    -- 方法fetch_log()
    -- 方法parse_log()
    -- 方法store_log()
    -- 方法statistics()，打印一个简短的统计信息（共成功解析到m条数据，成功写入数据库n条数据，m >= n）
3.main_max.py
(1) 解析一组endpoint，并写入数据库
(2) 主类为HeatMax
    -- 包装了HeatMain。添加循环处理每一个endpoint，每个处理创建一个HeatMian对象
    -- start()方法接收两个参数：endpoints和conn
(3) 辅助类HeatEndpoints
    -- 接收一个路径参数
    -- collect()方法返回endpoint的列表，即endpoints


4.TODO
(1) 有的地方捕捉到异常，可能应该continue，而不是raise
(2) 数据库信息，endpoint


