import sqlite3


# 创建携程数据库
conn = sqlite3.connect('xiecheng.db')

# 创建一个包含机票信息的表
# 分别是 公司名、出发时间、到达时间、出发机场、到达机场、飞机类型、准点率、飞机编号、价格、日期
CREATE_COMMAND1 = '''
CREATE table AIRPLANE (
    company_name varchar(1000),
    start_time varchar(1000),
    arrival_time varchar(1000),
    start_airport varchar(1000),
    arrival_airport varchar(1000),
    airpane_type varchar(1000),
    ontime_rate float,
    airpane_number varchar(1000),
    price float,
    date varchar(1000)
);
'''

# 选择预计，根据飞机编号、日期、出发时间选出需要的机票信息
SELECT_COMMAND = '''
select * from AIRPLANE where airpane_number=? and date=? and start_time=?;
'''

# 插入新的数据
INSERT_COMMAND1 = '''
insert into AIRPLANE values(?,?,?,?,?,?,?,?,?,?);
'''

# 创建一个最低价格的表，包含出发城市、到达城市、日期、最低价格
CREATE_COMMAND2 = '''
CREATE table LOWEST_PRICE (
    start_city varchar(1000),
    arrival_city varchar(1000),
    date varchar(1000),
    price float
);
'''

# 插入数据
INSERT_COMMAND2 = '''
insert into LOWEST_PRICE values(?,?,?,?);
'''

# 创建表
cursor = conn.cursor()
cursor.execute(CREATE_COMMAND1)
cursor.close()
cursor = conn.cursor()
cursor.execute(CREATE_COMMAND2)
cursor.close()
