import pandas as pd

def convert(file):
    df = pd.read_json(file)
    df1000 = df[:1000]
    df1000.to_hdf('user_study.h5', key='data')