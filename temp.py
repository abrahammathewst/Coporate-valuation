import pandas as pd

df = pd.read_csv(".\data\ind_nifty500list.csv")
print(df.columns.tolist())
print(df.head())
# print(df["ISIN Code"].tolist())