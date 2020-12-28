import time
import logging
from multiprocessing import Process

from src.logger import get_process_logger
from src.state import HeaterState

def _supervise(temp_is, temp_should, running, heating):
    state = HeaterState(temp_is=temp_is, should=temp_should, running=running, heating=heating)
    logger = get_process_logger('superviser')
    logger.log(logging.INFO, "Superviser process started")
    # TODO
    while(state.is_running()):
        print(state.get_temp_should())
#         # state.update_temp_is()
#         # temp_is_rounded = int(round(state.get_temp_is()))
#         # if (temp_is_rounded < (temp_should.value - temp_should.value * tolerance)):
#         #     turn_on_heating()
#         #     heating.value = True
#         # elif (temp_is_rounded >= temp_should.value):
#         #     turn_off_heating()
#         #     heating.value = False
#         # time.sleep(30)
#         time.sleep(1)

class Superviser():

    def __init__(self, state: HeaterState, logger: logging.Logger):
        self._superviser: Process = None
        self._state = state
        self._logger = logger

    def _start(self):
        try:
            self._superviser.start()
        except RuntimeError:
            self._superviser = None
            self._logger.log(logging.ERROR, "Cannot stop process - Process already running")
            return False

        return True

    def start(self) -> bool:
        if self._superviser == None:
            self._superviser = Process(target=_supervise,
                                       args=(self._state._temp_is,
                                             self._state._temp_should,
                                             self._state._running,
                                             self._state._heating))
            return self._start()
        self._logger.log(logging.WARNING, "Cannot start superviser twice")
        return False

    def stop(self) -> bool:
        try:
            self._superviser.join(timeout=5)
            if self._superviser is not None and self._superviser.is_alive():
                self._logger.log(logging.ERROR, "Cannot stop process - Still alive after timeout")
                return False
            self._superviser = None
            #self._state.turn_off_heating()
        except RuntimeError:
            self._logger.log(logging.ERROR, "Cannot stop process - Process wasn't running")
            return False

        return True



