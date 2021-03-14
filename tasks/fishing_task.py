import datetime
import random

import util
from consts import base_fish_frequency
from persistence.dto.fish import Fish
from persistence.fish_persistence import get_fish


def get_fishing_task_rewards(start_time: datetime, task_time: datetime.timedelta):
    start = int(start_time.timestamp())
    total_time = int(task_time.total_seconds())
    rewards = []
    if total_time < 5:
        return rewards
    for i in range(
        start + base_fish_frequency, start + total_time, base_fish_frequency
    ):
        fish = go_fish(i)
        if fish:
            rewards.append(fish)
    return rewards


def go_fish(time):
    if random.random() < 0.2:
        if random.random() < 0.2:
            return Fish(0, 0, "Trash", "", "", "", 0)
        else:
            t = datetime.datetime.fromtimestamp(time)
            ig_time = util.get_in_game_time(t)
            ig_weather = util.get_in_game_weather(t)
            return get_fish_from_table(ig_time, ig_weather)


def get_fish_from_table(ig_time: str, ig_weather: str):
    fish_table = get_fish(ig_time, ig_weather)
    return util.get_random_from_weighted_table(fish_table)
