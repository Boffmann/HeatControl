from flask_socketio import SocketIO, Namespace, emit

from src.state import HeaterState
from src.utils import round_dec_two

class StateSocket(Namespace):

    _state: HeaterState
    start_stop_superviser=None

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

    def on_temp_is_updated(self):
        self.publish_temp_is()

    def publish_state(self):
        emit('state', {'temp_should': round_dec_two(self._state.get_temp_should()), 'running': self._state.is_running(), 'heating': self._state.is_heating()}, broadcast=True)

    def publish_temp_is(self):
        emit('temp_is', {'temp_is': self._state.get_temp_is()}, broadcast=True)
