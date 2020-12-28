import sqlite3
import time

from src.config import DatabaseConfig

database_config = DatabaseConfig()


def get_curr_time():
    ts = time.time()
    return int(round(ts))

class DBConnection:

    def __init__(self):
        self._db_conn = sqlite3.connect(database_config['filename'])
        self._conn = self._db_conn.cursor()
        # Create table
        self._conn.execute("CREATE TABLE IF NOT EXISTS temps (date integer, temp real);")

    def insert_temp(self, temp: float):
        self._conn.execute("INSERT INTO temps VALUES (?, ?);", (get_curr_time(), temp))
        self._db_conn.commit()

    def close(self):
        self._db_conn.close()
