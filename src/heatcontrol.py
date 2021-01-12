import RPi.GPIO as GPIO
from typing import List
import board
import time
import glob

from src.config import InterfaceConfig

# TODO Error handling

interface_config = InterfaceConfig()

_FAN_PIN = interface_config['fan']
_HEATER_PIN = interface_config['heater']

GPIO.setup(_FAN_PIN, GPIO.OUT)
GPIO.setup(_HEATER_PIN, GPIO.OUT)

# Temp sensors use one wire protocol.
_base_dir = interface_config['temp_sensor_dir']
device_folder_1 = glob.glob(base_dir + '28*')[0]
device_file_1 = device_folder_1 + '/w1_slave'

def _read_temp_raw():
    """ Reads raw string values from the one wire files

    Returns:
    List of all lines from the one wire files
    """
    res = []
    f = open(device_file_1, 'r')
    res.append(f.readlines())
    f.close()
    return res

def get_temps -> List[float]:
    """ Extracts the parts from one wire file's content that encodes the temperature
    """
    res = []
    lines = read_temp_raw()
    while lines[0][0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[0][1].find('t=')
    if equals_pos != -1:
        temp_string = lines[0][1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        res.append(temp_c)

    return res

def get_temperature() -> float:
    """ Calculates the overall temperature by conculating mean value
    """
    temps = get_temps()

    return (temps[0] + temps[1]) / 2.0

def turn_on_heating():
    global _HEATER_PIN
    GPIO.output(_HEATER_PIN, GPIO.HIGH)

def turn_off_heating():
    global _HEATER_PIN
    GPIO.output(_HEATER_PIN, GPIO.LOW)

def turn_on_fan():
    global _FAN_PIN
    GPIO.output(_FAN_PIN, GPIO.HIGH)

def turn_off_fan():
    global _FAN_PIN
    GPIO.output(_FAN_PIN, GPIO.LOW)
