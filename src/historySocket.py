from flask_socketio import SocketIO, Namespace, emit

from src.state import HeaterState
from src.history import DBConnection

class HistorySocket(Namespace):

    _state: HeaterState
    _start_time: int

    def set_starttime(self, time: int):
        self._start_time = time

    def on_connect(self):
       print("History connected")

    def on_get_since_start(self):
        print("Since Start")
        db_conn = DBConnection()
        print(self._start_time)
        rows = db_conn.get_since(self._start_time)
        emit('since_start', {'values': rows})

        for row in rows:
           print(row)
        db_conn.close()

    def on_temp_is_updated(self):
        print("Got history")
        db_conn = DBConnection()
        temp_is = self._state.get_temp_is()
        db_conn.insert_temp(temp_is)
        emit('temp_is', {'temp_is': temp_is}, broadcast=True)
        db_conn.close()
