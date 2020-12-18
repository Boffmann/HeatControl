from typing import List
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3004 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

_SCK_PIN = board.SCK
_MISO_PIN = board.MISO
_MOSI_PIN = board.MOSI
_CS_PIN = board.D22
_RELAIS_PIN = 27

GPIO.setup(_RELAIS_PIN, GPIO.OUT)

# Create SPI Bus
_spi = busio.SPI(clock=_SCK_PIN, MISO=_MISO_PIN, MOSI=_MOSI_PIN)

# Creat Chip Select
_cs = digitalio.DigitalInOut(_CS_PIN)

# Create mcp object
_mcp = MCP.MCP3004(_spi, _cs)

# Create analog input channels
_channel0 = AnalogIn(_mcp, MCP.P0)
_channel1 = AnalogIn(_mcp, MCP.P1)
_channel2 = AnalogIn(_mcp, MCP.P2)
_channel3 = AnalogIn(_mcp, MCP.P3)

def __value_to_temperature(value):
    supply_voltage = 4.5
    max_digital_value = 64000
    factor = 100.0
    return (supply_voltage * (value / max_digital_value)) * factor

def get_temps() -> List[float]:
    global _channel0, _channel1, _channel2, _channel3

    ch0 = __value_to_temperature(_channel0.value)
    ch1 = __value_to_temperature(_channel1.value)
    ch2 = __value_to_temperature(_channel2.value)
    ch3 = __value_to_temperature(_channel3.value)

    return [ch0, ch1, ch2, ch3]

def get_temperature() -> float:
    temps = get_temps()

    return (temps[0] + temps[1] + temps[2] + temps[3]) / 4.0

def turn_on_heating():
    global _RELAIS_PIN
    GPIO.output(_RELAIS_PIN, GPIO.HIGH)

def turn_off_heating():
    global _RELAIS_PIN
    GPIO.output(_RELAIS_PIN, GPIO.LOW)
