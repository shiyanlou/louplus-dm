import pandas as pd


def data_clean():
    '''data_clean() 函数用于数据清洁，大致步骤如下：
    1. 统一设置国家代码为新索引
    2. 去掉多余的数据列
    3. 将不规范空值替换为 NaN，并进行填充
    '''
    # 读取数据文件
    df_data = pd.read_excel("ClimateChange.xlsx", sheetname='Data')
    df_country = pd.read_excel("ClimateChange.xlsx", sheetname='Country')

    # 处理 data 数据表
    # 选取 EN.ATM.CO2E.KT 数据，并将国家代码设置为索引
    df_data_reindex = df_data[df_data['Series code']== 'EN.ATM.CO2E.KT'].set_index('Country code')
    # 剔除不必要的数据列
    df_data_drop = df_data_reindex.drop(labels=['Country name', 'Series code', 'Series name', 'SCALE', 'Decimals'], axis=1)
    # 将原数据集中不规范的空值替换为 NaN 方便填充
    df_data_nan = df_data_drop.replace({'..': pd.np.NaN})
    # 对 NaN 空值进行向前和向后填充
    df_data_fill = df_data_nan.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    # 对填充后依旧全部为空值的数据行进行剔除
    df_data_dropna = df_data_fill.dropna(how='all')

    # 处理 Country 数据表
    # 将国家代码设置为索引
    df_country_reindex = pd.DataFrame(df_country).set_index('Country code')
    # 剔除不必要的数据列
    df_country_drop = df_country_reindex.drop(labels=['Capital city', 'Region', 'Lending category'], axis=1)

    # 合并数据表
    # 对 Data 和 Country 表按照索引进行合并
    df_combine = pd.concat([df_data_dropna, df_country_drop], axis=1)
    # 对合并后数据集进行求和得到各国排放总量
    df_combine['Sum emissions'] = df_combine[list(df_combine)[:-2]].sum(axis=1)
    # 对合并后存在空值的数据行进行剔除，得到清洁后的数据集
    df_clean = df_combine.dropna(thresh=10)

    return df_clean

def co2():
    '''co2() 函数用于数据统计，大致步骤如下：
    1. 使用 groupby 按题目规则求和
    2. 对数据进行排序并得到目标 DataFrame
    '''
    # 读取清洁后数据
    df_clean = data_clean()

    # 按收入群体对数据进行求和
    sum_by_groups = df_clean.groupby('Income group')['Sum emissions'].sum()

    # 按要求整理 DataFrame
    item_high_list = []
    item_low_list = []

    for group_name in list(sum_by_groups.index):
        # 得到各收入群体最高排放量数据
        item_high = df_clean[df_clean['Income group'] == group_name].sort_values(by='Sum emissions', ascending=False).iloc[0]
        # 将最高排放量数据存入相应列表方便生成最终 DataFrame
        item_high_list.append((item_high['Income group'], item_high['Country name'], item_high['Sum emissions']))
        # 得到各收入群体最低排放量数据
        item_low = df_clean[df_clean['Income group'] == group_name].sort_values(by='Sum emissions').iloc[0]
        # 将最低排放量数据存入相应列表方便生成最终 DataFrame
        item_low_list.append((item_low['Income group'], item_low['Country name'], item_low['Sum emissions']))

    # 设置 DataFrame 标签
    high_labels = ['Income group', 'Highest emission country', 'Highest emissions']
    low_labels = ['Income group', 'Lowest emission country', 'Lowest emissions']

    # 生成并合并目标 DataFrame
    highest_df = pd.DataFrame.from_records(item_high_list, columns=high_labels).set_index('Income group')
    lowest_df = pd.DataFrame.from_records(item_low_list, columns=low_labels).set_index('Income group')

    results = pd.concat([sum_by_groups, highest_df, lowest_df], axis=1)

    return results