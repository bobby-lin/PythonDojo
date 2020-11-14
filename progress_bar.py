import pandas as pd
import requests
import progressbar
import time
import numpy as np
from tqdm import tqdm


def get_profit_over_revenue_pct(revenue, profit):
    return profit / revenue


df = pd.read_csv("sample_data/sample_data_1M.csv")
tqdm.pandas(desc="Processing")
df['Profit/Revenue Pct'] = df.progress_apply(lambda row: get_profit_over_revenue_pct(row['Total Revenue'], row['Total Profit']), axis=1)
print(df.head(10))

for i in progressbar.progressbar(range(1000)):
    time.sleep(0.02)