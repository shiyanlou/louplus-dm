import numpy as np
import pandas as pd


def caculate_w():

    # 读取数据集
    df = pd.read_csv("nyc-east-river-bicycle-counts.csv", index_col=0)

    # 处理自变量
    x = df['Brooklyn Bridge'].values
    x = x.reshape(len(x), 1)  # 添加截距项系数
    x = np.matrix(np.concatenate((np.ones_like(x), x), axis=1))

    # 处理因变量
    y = df['Manhattan Bridge'].values
    y = np.matrix(y.reshape(len(y), 1))

    # 使用矩阵方法计算
    W = (x.T * x).I * x.T * y
    b = round(float(W[0]), 2)
    w = round(float(W[1]), 2)
    
    return w, b
