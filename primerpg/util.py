#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import datetime
import math
import random
from math import sin, pi
from typing import TypeVar, Dict

from numpy.random import normal

from primerpg.consts import day_night_cycles_per_day, weather_frequency, raining_weather, clear_weather

# Util constants
from primerpg.date_util import time_delta_to_str

base_xp_per_level = 100
increased_xp_per_level = 40
base_hp_per_level = 20
hp_loss_per_tier = 2


T = TypeVar("T")
U = TypeVar("U")


def get_current_in_game_time() -> str:
    now = datetime.datetime.utcnow()
    return get_in_game_time(now)


def get_in_game_time(time: datetime) -> str:
    delta = datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    new_delta = day_night_cycles_per_day * delta
    return time_delta_to_str(new_delta)


def get_current_in_game_weather() -> str:
    now = datetime.datetime.utcnow()
    return get_in_game_weather(now)


def get_in_game_weather(time: datetime) -> str:
    scaled_time = int(time.timestamp()) / weather_frequency
    humidity = 0.5 * (sin(2 * scaled_time) + sin(pi * scaled_time))
    if humidity > 0:
        return raining_weather
    else:
        return clear_weather


def get_random_from_weighted_list(weighted_list: list[T]) -> T:
    """Gets a random item from the list of objects, weighted by the "weight" property on each item

    :param weighted_list: List of objects with a weight property
    :return: An item from the list
    """
    total_weight = sum([x.weight for x in weighted_list])
    weight = random.randrange(total_weight)
    for item in weighted_list:
        if weight < item.weight:
            return item
        else:
            weight -= item.weight


def xp_at_level(level: int) -> int:
    """This method calculates the amount of xp required to go from the previous level to this level

    :param level: The level to calculate for
    :return: The amount of xp
    """
    if level <= 0:
        return 0
    return base_xp_per_level + increased_xp_per_level * (level - 1)


def req_xp_for_level(level: int) -> int:
    """This method calculates the total xp required to attain the given level.

    :param level: The level to calculate for
    :return: The amount of xp
    """
    if level <= 0:
        return 0
    return int(level * 0.5 * (xp_at_level(1) + xp_at_level(level)))


def level_from_total_xp(total_xp: int) -> int:
    return math.floor(
        equation_roots(
            increased_xp_per_level,
            2 * base_xp_per_level - increased_xp_per_level,
            -2 * total_xp,
        )
    )


def progress_to_next_level(total_xp: int) -> float:
    level = level_from_total_xp(total_xp)
    return (total_xp - req_xp_for_level(level)) / xp_at_level(level + 1)


def equation_roots(a, b, c):
    dis = b * b - 4 * a * c
    sqrt_val = math.sqrt(abs(dis))

    val1 = (-b + sqrt_val) / (2 * a)
    val2 = (-b - sqrt_val) / (2 * a)

    return max(val1, val2)


def calculate_max_hp(vitality: int) -> float:
    if vitality <= 0:
        return base_hp_per_level / 2
    if vitality < 50:
        tier = math.floor(vitality / 10)
        var_health = (vitality - 10 * tier) * (base_hp_per_level - hp_loss_per_tier * tier) + sum(
            [10 * (base_hp_per_level - hp_loss_per_tier * t) for t in range(tier)]
        )
    else:
        var_health = (vitality - 50) * (base_hp_per_level - hp_loss_per_tier * 5) + 800
    return float(var_health)


def roll_gaussian_dist_for_drop(mean: float, std_dev: float) -> float:
    drop_min = max(mean - 3 * std_dev, 1)
    drop_max = mean + 3 * std_dev
    return min(max(normal(mean, std_dev), drop_min), drop_max)


def get_key_for_value(dictionary: Dict[T, U], value: U) -> T:
    keys = list(dictionary.keys())
    vals = list(dictionary.values())

    position = vals.index(value)
    return keys[position]


def check_is_int(s):
    s = str(s)
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()
