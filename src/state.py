from multiprocessing import Value

from src.history import DBConnection
# from src.heatcontrol import get_temperature, turn_on_heating, turn_off_heating, get_temps

class HeaterState:

    def __init__(self, temp_is: Value('d'), should: Value('d'), running: Value('b'), heating: Value('b')):

        self._temp_is = temp_is
        self._temp_should = should
        self._running = running
        self._heating = heating

        self._temp_is.value = 20.0#get_temperature()
        self._db_conn = DBConnection()

    def is_running(self):
        return self._running.value

    def is_heating(self):
        return self._heating.value

    def get_temp_is(self):
        return self._temp_is.value

    def get_temp_should(self):
        return self._temp_should.value

    def update_temp_is(self):
        self._temp_is.value = 20.0#get_temperature()
        self._db_conn.insert_temp(self._temp_is.value)

    def increate_temp_should(self):
        self._temp_should.value += 1.0

    def decrease_temp_should(self):
        self._temp_should.value -= 1.0

    def toggle_running(self):
        self._running.value = not self._running.value

    def turn_off_heating(self):
        #turn_off_heating()
        self._heating.value = False

    def turn_on_heating(self):
        #turn_on_heating()
        self._heating.value = True
