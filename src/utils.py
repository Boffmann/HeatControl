import time

from src.config import EnvironmentConfig

env_config = EnvironmentConfig()

# Jouls / kilogram * Kelvin
_air_heat_capacity = 1000.0
# Kilograms / cubic meter
_air_density = 1.2

_heat_room_volume = env_config['box_width'] * env_config['box_height'] * env_config['box_depth']
_air_mass_in_room = _heat_room_volume * _air_density

_heater_power = env_config['heater_power']

def get_curr_time():
    ts = time.time()
    return int(round(ts))

def get_time_to_heat(temp_from: float, temp_to: float) -> float:
    """
    Get the time it takes to heat up the room from temp_from to temp_to in seconds
    """

    temp_diff = temp_to - temp_from
    if (temp_diff <= 0):
       return 0.0

    energy_required = _air_heat_capacity * _air_mass_in_room * temp_diff

    return energy_required / _heater_power
