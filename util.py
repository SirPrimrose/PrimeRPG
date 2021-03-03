import datetime

from consts import day_night_cycles_per_day


def get_in_game_time():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    new_delta = day_night_cycles_per_day * delta
    return new_delta
