import pandas as pd


def clean():
    # 读取数据
    df = pd.read_csv("earthquake.csv")
    # 选择需保留列
    df1 = df[['time', 'latitude', 'longitude', 'depth', 'mag']]
    # 对 place 列使用自定义分割，得到需要的 region 数据
    df2 = pd.DataFrame(df.place.str.split(', ', 1).tolist(),
                       columns=['address', 'region'])['region']
    # 拼接数据
    df = pd.concat([df1, df2], axis=1)
    # 去除重复值和缺失值行
    df_clean = df.drop_duplicates().dropna()
    
    return df_clean
