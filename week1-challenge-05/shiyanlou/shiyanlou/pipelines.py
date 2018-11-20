# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class ShiyanlouPipeline(object):

    def process_item(self, item, spider):
        # 读取 item 数据
        repo_name = item['repo_name']
        update_time = item['update_time']
        # 每条数据组成临时 df_temp
        df_temp = pd.DataFrame([[repo_name, update_time]], columns=['repo_name', 'update_time'])
        # 将 df_temp 合并到 df
        self.df = self.df.append(df_temp, ignore_index=True).sort_values(by=['update_time'], ascending=False)

        return item

    #当爬虫启动时
    def open_spider(self, spider):
        # 新建一个带列名的空白 df
        self.df = pd.DataFrame(columns=['repo_name', 'update_time'])

    # 当爬虫关闭时
    def close_spider(self, spider):
        # 将 df 存储为 csv 文件
        pd.DataFrame.to_csv(self.df, "../shiyanlou_repo.csv")
