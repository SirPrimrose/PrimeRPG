import datetime

from math import sin, pi

from consts import day_night_cycles_per_day


def get_in_game_time():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    new_delta = day_night_cycles_per_day * delta
    return new_delta


def get_in_game_weather(time):
    scaled_time = time / 6000
    humidity = 0.5 * (sin(2 * scaled_time) + sin(pi * scaled_time))
    if humidity > 0:
        return 'raining'
    else:
        return 'clear'
