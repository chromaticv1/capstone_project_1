import os
import pandas as pd
def collect_df(category, index):
    cwd = os.getcwd()
    file_path = cwd + f'\\data\\raw_tables\\{category}\\{index}.csv'
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else: return None