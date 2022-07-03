import pandas as pd
import sqlite3

df = pd.read_excel(r'../data_set.xlsx', header=None)[3:]
conn = sqlite3.connect('../db/info_cve.db')
c = conn.cursor()
df.to_sql('full_info', conn, if_exists='replace', index=False, index_label=None)
