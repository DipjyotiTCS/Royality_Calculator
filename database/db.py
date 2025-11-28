import sqlite3

def get_db_connection():
    conn = sqlite3.connect("local_sales_db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn