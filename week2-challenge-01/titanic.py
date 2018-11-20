from matplotlib import pyplot as plt
import seaborn as sns

def plot():
    df = sns.load_dataset("titanic")

    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(15,4))

    sns.distplot(df.age.dropna(), ax=axes[0])
    sns.countplot(x='sex', hue="alive", data=df, ax=axes[1])
    sns.countplot(x="class", hue="alive", data=df, ax=axes[2])

    return axes