from flask_socketio import Namespace, emit

from heatcontrol.test_state import HeaterState
from heatcontrol.superviser import Superviser
from heatcontrol.utils import get_curr_time
from heatcontrol.history import DBConnection
from heatcontrol.utils import get_curr_time

class StateSocket(Namespace):

    _state: HeaterState
    _superviser: Superviser
    _start_time: int

    def initialize(self, state: HeaterState):
        self._state = state
        self._superviser = Superviser(state=state)

    def on_connect(self):
        print("Connected")
        self._publish_state()

    def on_disconnect(self):
        print("Disconnected")

    def on_raise(self):
        self._state.increate_temp_should()
        self._publish_state()

    def on_lower(self):
        self._state.decrease_temp_should()
        self._publish_state()

    def on_onoff(self):
        is_running = self._state.toggle_running()
        if is_running:
            if self._superviser.start():
                self._start_time = get_curr_time()
        else:
            self._superviser.stop()

        self._publish_state()

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
        self._publish_state()

    def _publish_state(self):
        emit('state', {'temp_should': self._state.get_temp_should(), 'running': self._state.is_running(), 'heating': self._state.is_heating()}, broadcast=True)
