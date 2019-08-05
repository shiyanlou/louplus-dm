import pandas as pd


def clean():
    # 读取据
    df = pd.read_csv("earthquake.csv")
    # 选择需保留列
    df1 = df[['time', 'latitude', 'longitude', 'depth', 'mag']]
    # 对 place 列使用分割，得到需要的 region 数据
    place = df.place.str.split(', ').tolist()
    region = []
    for row in place:
        region.append(row[-1])
    df2 = pd.DataFrame(region, columns=['region'])
    # 拼接数据
    df = pd.concat([df1, df2], axis=1)
    # 去除重复值
    df_clean = df.drop_duplicates().dropna()

    return df_clean