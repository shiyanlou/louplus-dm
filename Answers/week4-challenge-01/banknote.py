import pandas as pd
import numpy as np
from sklearn.svm import SVC

def identify():

    df_train = pd.read_csv("banknote_train.csv")
    df_test = pd.read_csv("banknote_test.csv")

    model = SVC(gamma='auto')
    model.fit(df_train.iloc[:, :-1], df_train['class'])
    df_test['class'] = model.predict(df_test)

    return df_test