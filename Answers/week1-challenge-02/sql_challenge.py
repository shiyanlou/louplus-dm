import sqlite3
import pandas as pd

def count(file, user_id):

    sql_con = sqlite3.connect(file)
    sql_query = "SELECT * FROM data WHERE user_id == {}".format(user_id)
    df = pd.read_sql(sql_query, sql_con)

    if len(df)==0:
        return 0
    else:
        sum_minutes = df.minutes.sum()
        return sum_minutes