import datetime
import random

import util
from consts import base_fish_frequency
from persistence.persistence import get_fish_data


def get_fishing_task_rewards(start_time: datetime, task_time: datetime.timedelta):
    start = int(start_time.timestamp())
    total_time = int(task_time.total_seconds())
    rewards = []
    if total_time < 5:
        return rewards
    for i in range(start + base_fish_frequency, start + total_time, base_fish_frequency):
        fish = go_fish(i)
        if fish:
            rewards.append(fish)
    return rewards


def go_fish(time):
    print('Fishing tick: {}'.format(time))
    if random.random() < 0.2:
        if random.random() < 0.2:
            # Trash
            return {'id': 0, 'name': 'Trash'}
        else:
            # Fish
            # Select all fish we can catch, then roll weight table
            t = datetime.datetime.fromtimestamp(time)
            ig_time = util.get_in_game_time(t)
            ig_weather = util.get_in_game_weather(t)
            return get_fish_from_table(ig_time, ig_weather)


def get_fish_from_table(ig_time, ig_weather):
    fish_table = get_fish_data(ig_time, ig_weather)
    print(fish_table)
    return {'id': 1, 'name': 'Carp'}
