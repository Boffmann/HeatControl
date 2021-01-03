import time
from multiprocessing import Process
from enum import Enum

import src.logging as mylogger
from src.state import HeaterState

class Phase(Enum):
    PREHEAT = 1
    APPROACH_HEAT = 2
    KEEP_HEAT = 3

# TODO inform about changed heating variable
def _supervise(temp_is, temp_should, running, heating):
    state = HeaterState(temp_is=temp_is, should=temp_should, running=running, heating=heating)
    state.connect_to_socket()
    mylogger.info("Superviser process started")

    state.update_temp_is()
    if (state.should_preheat()):
        phase = Phase.PREHEAT
    elif (state.should_approach_heat()):
        phase = Phase.APPROACH_HEAT
    else:
        phase = Phase.KEEP_HEAT

    while(state.is_running()):
        state.update_temp_is()

        if (phase == Phase.PREHEAT):
            if (state.should_preheat()):
                state.turn_on_heating()
                state.turn_on_fan()
                time.sleep(state.get_time_to_heat(4.0))
            elif (state.should_approach_heat()):
                phase = Phase.APPROACH_HEAT
            else:
                phase = Phase.KEEP_HEAT
        elif (phase == Phase.APPROACH_HEAT):
            if (state.should_preheat()):
                phase = Phase.PREHEAT
            elif (state.should_approach_heat()):
                state.turn_on_heating()
                state.turn_on_fan()
                time.sleep(state.get_time_to_heat(1.0))
            else:
                phase = Phase.KEEP_HEAT
        else: # KEEP_HEAT
            if (state.should_preheat()):
                phase = Phase.PREHEAT
            elif (state.should_approach_heat()):
                phase = Phase.APPROACH_HEAT
            else:
                time_heating = state.get_time_to_reach(state.get_temp_should())
                if (time_heating <= 0.5):
                    state.turn_off_heating()
                    state.turn_off_fan()
                    time.sleep(60)
                    continue
                state.turn_on_heating()
                state.turn_on_fan()
                time.sleep(time_heating)
                state.turn_off_heating()
                time.sleep(20)
                state.turn_off_fan()
                time.sleep(600 - 20 - time_heating)

class Superviser():

    def __init__(self, state: HeaterState):
        self._superviser: Process = None
        self._state = state

    def _start(self):
        try:
            self._superviser.start()
        except RuntimeError:
            self._superviser = None
            mylogger.error("Cannot stop process - Process already running")
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
        mylogger.warning("Cannot start superviser twice")
        return False

    def stop(self) -> bool:
        try:
            self._superviser.terminate()
            self._superviser.join(timeout=5)
            if self._superviser is not None and self._superviser.is_alive():
                mylogger.error("Cannot stop process - Still alive after timeout")
                return False
            self._superviser = None
            #self._state.turn_off_heating()
        except RuntimeError:
            mylogger.error("Cannot stop process - Process wasn't running")
            return False

        return True



