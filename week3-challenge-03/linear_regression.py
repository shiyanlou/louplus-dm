import numpy as np
import pandas as pd


def gradient_descent():
    # 读取数据集
    df = pd.read_csv("nyc-east-river-bicycle-counts.csv", index_col=0)
    # 读取自变量
    x = df['Brooklyn Bridge'].values
    # 读取因变量
    y = df['Manhattan Bridge'].values

    w = 0  # 初始参数为 0
    b = 0  # 初始参数为 0
    lr = 0.000000001  # 学习率
    num_iter = 1000  # 迭代次数
    for i in range(num_iter):  # 梯度下降迭代
        # 计算近似值
        y_hat = (w * x) + b
        # 计算参数对应梯度
        w_gradient = -(2/len(x)) * sum(x * (y - y_hat))
        b_gradient = -(2/len(x)) * sum(y - y_hat)
        # 根据梯度更新参数
        w -= lr * w_gradient
        b -= lr * b_gradient

    return w, b
