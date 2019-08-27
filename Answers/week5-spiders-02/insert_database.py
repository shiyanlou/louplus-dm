import datetime
import pandas as pd


base = datetime.date(2018, 10, 30)
numdays = 80

# 所有的十月三十号以后的八十天的 list
date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]

# 获取从 start 到 dest 的数据并插入数据库中
def getTickets(start, dest, driver, date_list, conn):
    cursor = conn.cursor()
    name_attribute = []
    for one_day in tqdm_notebook(date_list):
        # 获取数据
        tmp = get_ticket_info(start, dest, str(one_day), driver)
        for x in tmp:
            result = cursor.execute(
                SELECT_COMMAND, (x[-2], str(one_day), x[1])).fetchall()
            x.append(str(one_day))
            if len(result) == 0:
                # 如果没有爬取则插入数据库
                cursor.execute(INSERT_COMMAND1, x)
                conn.commit()
    cursor.close()


# 成都到上海和上海到成都
getTickets('CTU', 'SHA', driver, date_list, conn)
getTickets('SHA', 'CTU', driver, date_list, conn)
