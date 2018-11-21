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


def mag_region():
    # 加载清洁后数据
    df_clean = clean()
    # 数据离散化，注意开闭区间
    df_clean['mag'] = pd.cut(df_clean.mag, bins=[0, 2, 5, 7, 9, 15], right=False, labels=[
                             'micro', 'light', 'strong', 'major', 'great'])
    
    print(df_clean)
    # 多索引分组聚合并计数
    df_group = df_clean.groupby(by=['mag', 'region']).count()
    # 重置索引并去除缺失值
    df_reindex = df_group.reset_index().dropna()
    # 按计数从大到小排序，并使用去除重复值的方法巧妙地保留下各地区最大值
    df_sort = df_reindex.sort_values(
        by='time', ascending=False).drop_duplicates(['mag'])
    # 按题目要求整理并重命名
    df_final = df_sort.set_index('mag')[['region', 'time']].rename(
        columns={"time": "times"})
    # 按题目要求将计数处理成 int 类型
    df_final['times'] = df_final.times.astype('int')

    return df_final
