import sqlite3
from datetime import datetime
import os

path = os.path.dirname(__file__)


class SQLite3:
    conn = sqlite3.connect(f"{path}/morax.db")
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS sales (timestamp int, sale int)")
    finally:
        conn.commit()

    @classmethod
    def insertData(cls, sale: int, date):
        time_stamp = datetime.timestamp(datetime.strptime(date, "%Y-%m-%d"))
        cls.cur.execute("INSERT INTO sales VALUES(?, ?)", (time_stamp, sale))
        return cls.conn.commit()

    @classmethod
    def getSale(cls, rowid: int) -> int:
        result = cls.cur.execute("SELECT sale FROM sales WHERE rowid={}".format(rowid))
        return result.fetchone()[0]

    @classmethod
    def getDate(cls):
        result = cls.cur.execute("SELECT timestamp, rowid FROM sales")
        return result.fetchall()

    @classmethod
    def getDateByRowid(cls, rowid: int) -> str:
        result = cls.cur.execute("SELECT timestamp FROM sales WHERE rowid={}".format(rowid))
        return result.fetchone()[0]

    @classmethod
    def removeData(cls, rowid: int):
        cls.cur.execute("DELETE FROM sales WHERE rowid={}".format(rowid))
        return cls.conn.commit()
