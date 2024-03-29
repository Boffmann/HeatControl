from multiprocessing import Value
import socketio

from src.heatcontrol import get_temperature, turn_on_heating_f, turn_off_heating_f, get_temps, turn_on_fan_f, turn_off_fan_f
from src.utils import get_time_to_heat

class HeaterState:

    def __init__(self, temp_is: Value('d'), should: Value('d'), running: Value('b'), heating: Value('b')):

        self._temp_is = temp_is
        self._temp_should = should
        self._running = running
        self._heating = heating

        self._socket = socketio.Client()

        self._temp_is.value = get_temperature()

    def connect_to_socket(self):
        self._socket.connect("http://localhost:80", namespaces=['/state'])

    def is_running(self):
        return self._running.value

    def is_heating(self):
        return self._heating.value

    def get_temp_is(self):
        return self._temp_is.value

    def should_preheat(self):
        return self.get_temp_is() < self.get_temp_should() - 5.0

    def should_approach_heat(self):
        return (self.get_temp_is() >= self.get_temp_should() - 5.0
                and self.get_temp_is() <  self.get_temp_should())

    def get_temp_should(self):
        return self._temp_should.value

    def update_temp_is(self):
        self._temp_is.value = get_temperature()
        self._socket.emit('temp_is_updated', namespace='/state')

    def increate_temp_should(self):
        self._temp_should.value += 1.0

    def decrease_temp_should(self):
        self._temp_should.value -= 1.0

    def toggle_running(self):
        self._running.value = not self._running.value

    def turn_off_heating(self):
        if not self._running.value:
            return
        turn_off_heating_f()
        self._heating.value = False
        self._socket.emit('heating', namespace='/state')

    def turn_on_heating(self):
        if not self._running.value:
            return
        turn_on_heating_f()
        self._heating.value = True
        self._socket.emit('heating', namespace='/state')

    def turn_on_fan(self):
        if not self._running.value:
            return
        turn_on_fan_f()

    def turn_off_fan(self):
        if not self._running.value:
            return
        turn_off_fan_f()

    def get_time_to_heat(self, temp_delta: float):
        return get_time_to_heat(self.get_temp_is(), self.get_temp_is() + temp_delta)

    def get_time_to_reach(self, temp: float):
        return get_time_to_heat(self.get_temp_is(), temp)
