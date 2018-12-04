import pandas as pd
from statsmodels.tsa.stattools import arma_order_select_ic


def arima():
    df = pd.read_csv("agriculture.csv", index_col=0)
    diff = df.diff().dropna()
    p, q = arma_order_select_ic(diff, ic='aic')['aic_min_order']  # AIC
    d = 1
    return p, d, q
