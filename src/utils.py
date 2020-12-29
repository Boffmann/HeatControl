import time

def round_dec_two(value: float):
    return round(value, 2)

def get_curr_time():
    ts = time.time()
    return int(round(ts))

