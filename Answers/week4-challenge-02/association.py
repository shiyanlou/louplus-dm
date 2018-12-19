import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules as rules

def rule():

    df = pd.read_csv("shopping_data.csv", header=None)
    dataset = df.stack().groupby(level=0).apply(list).tolist()

    te = TransactionEncoder()  # 定义模型
    te_ary = te.fit_transform(dataset)  # 转换数据集
    df = pd.DataFrame(te_ary, columns=te.columns_)  # 将数组处理为 DataFrame

    frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
    association_rules = rules(frequent_itemsets, metric="confidence", min_threshold=0.2) # 置信度阈值为 0.1
    
    return frequent_itemsets, association_rules