import pandas as pd
from pathlib import Path


file_path = Path("data") / "ind_company_list.csv"
df = pd.read_csv(file_path)
print(df.columns.tolist())
print(df.head())
# print(df["ISIN Code"].tolist())