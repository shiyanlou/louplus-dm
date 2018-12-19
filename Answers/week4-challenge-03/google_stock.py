import pandas as pd


def quarter_volume():
    df = pd.read_csv("GOOGL.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    df = df.resample('Q').agg({"Open": 'mean', "High": 'mean', "Low": 'mean',
                               "Close": 'mean', "Adj Close": 'mean', "Volume": 'sum'})
    df = df.sort_values(by='Volume', ascending=False)
    return df