import datetime

from math import sin, pi

from consts import day_night_cycles_per_day, raining_weather, clear_weather, weather_frequency


def get_current_in_game_time():
    now = datetime.datetime.utcnow()
    return get_in_game_time(now)


def get_in_game_time(time):
    delta = datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    new_delta = day_night_cycles_per_day * delta
    return new_delta


def get_current_in_game_weather():
    now = datetime.datetime.utcnow()
    return get_in_game_weather(now)


def get_in_game_weather(time):
    scaled_time = int(time.timestamp()) / weather_frequency
    humidity = 0.5 * (sin(2 * scaled_time) + sin(pi * scaled_time))
    if humidity > 0:
        return raining_weather
    else:
        return clear_weather


def time_delta_to_str(time_d: datetime.timedelta):
    hours, remainder = divmod(time_d.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


async def safe_send(msg, response):
    if len(response) > 2000:
        response = response[0:1999]
    await msg.channel.send(response)
