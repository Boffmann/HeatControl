import sqlite3

from src.config import DatabaseConfig
from src.utils import get_curr_time

database_config = DatabaseConfig()


class DBConnection:

    def __init__(self):
        self._db_conn = sqlite3.connect(database_config['filename'])
        self._conn = self._db_conn.cursor()
        # Create table

    def prepare_tables(self):
        self._conn.execute("CREATE TABLE IF NOT EXISTS temps (date integer, temp real);")

    def insert_temp(self, temp: float):
        self._conn.execute("INSERT INTO temps VALUES (?, ?);", (get_curr_time(), temp))
        self._db_conn.commit()

    def get_since(self, timestamp: int):
        print("Get since DB")
        # self._conn.execute("SELECT * FROM temps;")
        self._conn.execute("SELECT date, temp FROM temps WHERE date >= ? ORDER BY date ASC;", (timestamp,))
        print("Selected")
        return self._conn.fetchall()

    def close(self):
        self._db_conn.close()
