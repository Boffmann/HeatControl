from multiprocessing import Value
import socketio

class HeaterState:

    def __init__(self, temp_is: Value('d'), should: Value('d'), running: Value('b'), heating: Value('b')):

        self._temp_is = temp_is
        self._temp_should = should
        self._running = running
        self._heating = heating

        self._socket = socketio.Client()
        self._connected = False

        self._temp_is.value = 25

    def connect_to_socket(self):
        if self._connected:
            return
        self._socket.connect("http://localhost:80", namespaces=['/state'])
        self._connected = True
        print("Connected to socket")

    def disconnect_from_socket(self):
        if not self._connected:
            return
        self._socket.disconnect()
        self._connected = False
        print("Disconnected from socket")

    def is_running(self):
        return self._running.value

    def is_heating(self):
        return self._heating.value

    def get_temp_is(self):
        return self._temp_is.value

    def get_temp_should(self):
        return self._temp_should.value

    def update_temp_is(self):
        self._temp_is.value = self._temp_is.value + 1
        self._socket.emit('temp_is_updated', namespace='/state')

    def increate_temp_should(self):
        self._temp_should.value += 1.0

    def decrease_temp_should(self):
        self._temp_should.value -= 1.0

    def toggle_running(self):
        self._running.value = not self._running.value
        return self._running.value

    def turn_off_heating(self):
        print("Turned off heating")
        self._heating.value = False
        self._socket.emit('heating', namespace='/state')

    def turn_on_heating(self):
        if not self._running.value:
            print("Cannot turn on heating when not running")
            return
        print("Turned on heating")
        self._heating.value = True
        self._socket.emit('heating', namespace='/state')

    def turn_on_fan(self):
        if not self._running.value:
            print("Cannot turn on fan when not running")
            return
        print("Turned on fan")

    def turn_off_fan(self):
        print("Turned off fan")
