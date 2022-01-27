import sqlite3
import traceback
import sys

from src.config import DatabaseConfig
import src.logging as mylogger

database_config = DatabaseConfig()

class DBConnection:
    """
    Used to write and read temperature values from database file
    """

    def __init__(self):
        try:
            self._db_conn = sqlite3.connect(database_config['filename'])
            self._conn = self._db_conn.cursor()
        except:
            mylogger.error("Error opening the database connection - abort")

    def _execute(self, command, args=None):
        try:
            if args != None:
                self._conn.execute(command, args)
            else:
                self._conn.execute(command)
            self._db_conn.commit()
        except sqlite3.Error as er:
            mylogger.error('SQLite error: %s' % (' '.join(er.args)))
            mylogger.error("Exception class is: ", er.__class__)
            mylogger.error('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            mylogger.error(traceback.format_exception(exc_type, exc_value, exc_tb))

    def prepare_tables(self):
        """ 
        Create new temps table if it does not currently exist in database file
        """
        self._execute("CREATE TABLE IF NOT EXISTS temps (date integer, temp real, should real);")

    def insert_temp(self, timestamp: int, temp: float, should: float):
        self._execute("INSERT INTO temps VALUES (?, ?, ?);", (timestamp, temp, should))

    def get_since(self, timestamp: int):
        self._execute("SELECT date, temp, should FROM temps WHERE date >= ? ORDER BY date ASC;", (timestamp,))
        return self._conn.fetchall()

    def close(self):
        self._db_conn.close()
