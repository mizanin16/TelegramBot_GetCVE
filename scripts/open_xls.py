import os

import pandas as pd
import sqlite3

"""Данный пакет необходим для добавления записей в БД"""

base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
data_set = os.path.abspath(os.path.join(base_dir, 'db', 'data_set.xlsx'))
file_db = os.path.abspath(os.path.join(base_dir, 'db', 'info_cve.db'))


def to_sql_excel():
    """
    Занесение в БД данных
    """
    # todo: Реализовать поиск по расширению
    if os.path.exists(data_set):
        df = pd.read_excel(data_set, header=None)[3:]

        conn = sqlite3.connect(file_db)
        c = conn.cursor()
        df.to_sql('full_info', conn, if_exists='replace', index=False, index_label=None)
        print("File BD success save!")
    else:
        print('File for BD not exist')
