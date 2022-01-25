from flask_socketio import SocketIO, Namespace, emit

from src.state import HeaterState
from src.utils import round_dec_two, get_curr_time
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
        self.start_stop_superviser()
        self.publish_state()

    def on_get_since_start(self):
        db_conn = DBConnection()
        rows = db_conn.get_since(self._start_time)
        emit('since_start', {'values': rows})
        db_conn.close()

    def on_temp_is_updated(self):
        db_conn = DBConnection()
        temp_is = self._state.get_temp_is()
        temp_should = self._state.get_temp_should()
        curr_time = get_curr_time()
        db_conn.insert_temp(curr_time, temp_is, temp_should)
        emit('temps', {'timestamp': curr_time, 'temp_is': temp_is, 'temp_should': temp_should}, broadcast=True)
        db_conn.close()

    def on_heating(self):
        self.publish_state()

    def publish_state(self):
        emit('state', {'temp_should': round_dec_two(self._state.get_temp_should()), 'running': self._state.is_running(), 'heating': self._state.is_heating()}, broadcast=True)
