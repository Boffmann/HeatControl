import time

from src.config import EnvironmentConfig

env_config = EnvironmentConfig()

# Jouls / kilogram * Kelvin
air_heat_capacity = 1000.0
# Kilograms / cubic meter
air_density = 1.2

heat_room_volume = env_config['box_width'] * env_config['box_height'] * env_config['box_depth']
air_mass_in_room = heat_room_volume * air_density

heater_power = env_config['heater_power']

def round_dec_two(value: float):
    return round(value, 2)

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

    energy_required = air_heat_capacity * air_mass_in_room * temp_diff

    return energy_required / heater_power
