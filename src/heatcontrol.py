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
base_dir = interface_config['temp_sensor_dir']
device_folder_1 = glob.glob(base_dir + '28*')[0]
device_file_1 = device_folder_1 + '/w1_slave'
device_folder_2 = glob.glob(base_dir + '28*')[1]
device_file_2 = device_folder_2 + '/w1_slave'

def read_temp_raw():
    """ 
    Reads raw string values from the one wire files

    Returns:
    List of all lines from the one wire files
    """
    res = []
    f = open(device_file_1, 'r')
    res.append(f.readlines())
    f.close()
    f = open(device_file_2, 'r')
    res.append(f.readlines())
    f.close()
    return res

def get_temps() -> List[float]:
    """ 
    Extracts the parts from one wire file's content that encodes the temperature
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
    while lines[1][0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1][1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        res.append(temp_c)

    return res

def get_temperature() -> float:
    """ 
    Calculates the overall temperature by conculating mean value. Rounds result to two digits after comma
    """
    temps = get_temps()
    mean_temp = (temps[0] + temps[1]) / 2.0
    return round(mean_temp, 2)

def turn_on_heating_f():
    # Force turning on heating
    global _HEATER_PIN
    GPIO.output(_HEATER_PIN, GPIO.HIGH)

def turn_off_heating_f():
    # Force turning off heating
    global _HEATER_PIN
    GPIO.output(_HEATER_PIN, GPIO.LOW)

def turn_on_fan_f():
    # Force turning on fan
    global _FAN_PIN
    GPIO.output(_FAN_PIN, GPIO.HIGH)

def turn_off_fan_f():
    # Force turning off fan
    global _FAN_PIN
    GPIO.output(_FAN_PIN, GPIO.LOW)
