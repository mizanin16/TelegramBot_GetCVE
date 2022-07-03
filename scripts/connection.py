import os
import sqlite3

dir_db = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(dir_db)
conn = sqlite3.connect(os.path.join(BASE_DIR, "db", "info_cve.db"))

cursor = conn.cursor()


def get_info_fetchall(text, type_where) -> list:
    if '#TypeSystem' == type_where:
        if text != '':
            text = f'WHERE "7" LIKE "%{text.title()}%" '
    if '#NameProgramm' == type_where:
        if text != '':
            text = f'WHERE "4" LIKE "%{text.title()}%" '
    if '#NameVulnerability' == type_where:
        if text != '':
            text = f'WHERE "1" LIKE "%{text.title()}%" or "2" LIKE "%{text.title()}%" '
    sql_req = f"SELECT * FROM full_info {text}"
    print(sql_req)
    cursor.execute(sql_req)
    rows = cursor.fetchall()
    return rows
