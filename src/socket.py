from flask_socketio import SocketIO, Namespace, emit

from src.state import HeaterState
from src.utils import round_dec_two
from src.history import DBConnection

class StateSocket(Namespace):

    _state: HeaterState
    start_stop_superviser=None
    _start_time: int

    def set_starttime(self, time: int):
        self._start_time = time

    def on_connect(self):
        print("Connected")
        self.publish_state()

    def on_disconnect(self):
        print("Disconnected")

    def on_raise(self):
        self._state.increate_temp_should()
        self.publish_state()

    def on_lower(self):
        self._state.decrease_temp_should()
        self.publish_state()

    def on_onoff(self):
        self._state.toggle_running()
        self._start_stop_superviser()
        self.publish_state()

    def on_get_since_start(self):
        db_conn = DBConnection()
        rows = db_conn.get_since(self._start_time)
        emit('since_start', {'values': rows})

        for row in rows:
           print(row)
        db_conn.close()

    def on_temp_is_updated(self):
        db_conn = DBConnection()
        temp_is = self._state.get_temp_is()
        db_conn.insert_temp(temp_is)
        emit('temp_is', {'temp_is': temp_is}, broadcast=True)
        db_conn.close()

    def publish_state(self):
        emit('state', {'temp_should': round_dec_two(self._state.get_temp_should()), 'running': self._state.is_running(), 'heating': self._state.is_heating()}, broadcast=True)
