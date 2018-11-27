import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def beijing(n):

    # 读取数据，去除重复值，无空值
    df = pd.read_csv("beijing_house_price.csv")
    df = df.drop_duplicates()
    # df = df[['公交', '写字楼', '医院', '商场', '地铁', '学校', '建造时间', '楼层', '面积', '每平米价格']]
    df = df.iloc[:, [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]]  # 线上环境中文输入不方便

    # 计算特征与目标值相关性系数，并保留前 3 个特征
    pearson = np.abs(df.corr(method='pearson').iloc[-1])
    pearson_max = pearson.sort_values(ascending=False)[1:4]
    features_names = pearson_max.index.values
    features = df[features_names]
    # target = df['每平米价格']
    target = df.iloc[:, [9]]

    # 切分训练和测试数据
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.3, random_state=10)

    # 多项式特征处理
    poly_features = PolynomialFeatures(degree=n)
    X_train_features = poly_features.fit_transform(X_train)
    X_test_features = poly_features.fit_transform(X_test)

    # 建立线性回归模型
    model = LinearRegression()
    model.fit(X_train_features, y_train)
    y_pred = model.predict(X_test_features)

    # 计算平均绝对误差
    mae = mean_absolute_error(y_test, y_pred)

    return mae
