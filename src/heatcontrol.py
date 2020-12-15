import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3004 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

SCK_PIN = board.SCK
MISO_PIN = board.MISO
MOSI_PIN = board.MOSI
CS_PIN = board.D22
RELAIS_PIN = 27

SPIO.setup(RELAIS_PIN, GPIO.OUT)

# Create SPI Bus
spi = busio.SPI(clock=SCK_PIN, MISO=MISO_PIN, MOSI=MOSI_PIN)

# Creat Chip Select
cs = digitalio.DigitalInOut(CS_PIN)

# Create mcp object
mcp = MCP.MCP3004(spi, cs)

# Create analog input channels
channel0 = AnalogIn(mcp, MCP.P0)
channel1 = AnalogIn(mcp, MCP.P1)
channel2 = AnalogIn(mcp, MCP.P2)
channel3 = AnalogIn(mcp, MCP.P3)

def __value_to_temperature(value):
    return value * 100.0

def get_temperature():
    ch0 = __value_to_temperature(channel0.value)
    ch1 = __value_to_temperature(channel1.value)
    ch2 = __value_to_temperature(channel2.value)
    ch3 = __value_to_temperature(channel3.value)

    return (ch0 + ch1 + ch2 + ch3) / 4.0

def turn_on_heating():
    GPIO.output(RELAIS_PIN, GPIO.HIGH)

def turn_off_heating():
    GPIO.output(RELAIS_PIN, GPIO.LOW)
