import pandas as pd
from fbprophet import Prophet


def additive():
    df = pd.read_csv("Chengdu_HourlyPM25.csv")
    df_nan = df.replace({-999: pd.np.NaN})
    df = df_nan.fillna(method='ffill').fillna(method='bfill')

    df.index = pd.to_datetime(df['Date (LST)'])
    df = df.resample('D').mean()
    df = df.reset_index()
    df.rename(columns={'Date (LST)': 'ds', 'Value': 'y'}, inplace=True)

    m = Prophet()  # 创建加法模型
    m.fit(df)

    future = m.make_future_dataframe(periods=365, freq='D')  # 生成预测序列
    forecast = m.predict(future)  # 预测
    # 仅保留预测值和相应的置信区间
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast = forecast.set_index('ds')['2017-01-01':]

    forecast.to_csv("forecast.csv")  # 存为数据文件

    return forecast

additive()