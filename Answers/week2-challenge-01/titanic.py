from matplotlib import pyplot as plt
import seaborn as sns

def plot():
    df = sns.load_dataset("titanic")

    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(15,4))
    # 后续高版本的 Seaborn 中的 distplot 不支持 ax 参数，建议使用 histplot
    sns.distplot(df.age.dropna(), ax=axes[0])
    sns.countplot(x='sex', hue="alive", data=df, ax=axes[1])
    sns.countplot(x="class", hue="alive", data=df, ax=axes[2])

    return axes
