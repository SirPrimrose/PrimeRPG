import datetime
import math
import random
from math import sin, pi
from typing import List

from numpy.random import normal

from consts import (
    day_night_cycles_per_day,
    raining_weather,
    clear_weather,
    weather_frequency,
)
from persistence.dto.skill_category import SkillCategory
from persistence.skill_categories_persistence import get_all_skill_categories

# Util constants
does_not_exist_string = "DNE"
base_xp_per_level = 100
increased_xp_per_level = 40
base_hp_per_level = 20
hp_loss_per_tier = 2

# Preloaded data
skill_categories: List[SkillCategory] = []


def load_util_data() -> None:
    global skill_categories
    skill_categories = get_all_skill_categories()


def get_skill_category_name(skill_id: int) -> str:
    """Gets the skill category name without hitting the database

    :param skill_id: Unique id of the skill category
    :return: The name of the skill category, or "DNE" if it does not exist
    """
    try:
        return next(
            filter(lambda skill: skill.unique_id == skill_id, skill_categories)
        ).name
    except StopIteration:
        return does_not_exist_string


def get_skill_category_short_name(skill_id: int) -> str:
    """Gets the skill category short name without hitting the database

    :param skill_id: Unique id of the skill category
    :return: The name of the skill category, or "DNE" if it does not exist
    """
    try:
        return next(
            filter(lambda skill: skill.unique_id == skill_id, skill_categories)
        ).short_name
    except StopIteration:
        return does_not_exist_string


def get_current_in_game_time() -> str:
    now = datetime.datetime.utcnow()
    return get_in_game_time(now)


def get_in_game_time(time: datetime) -> str:
    delta = datetime.timedelta(
        hours=time.hour, minutes=time.minute, seconds=time.second
    )
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


def time_delta_to_str(time_d: datetime.timedelta):
    hours, remainder = divmod(time_d.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


async def safe_send(msg, response):
    if len(response) > 2000:
        response = response[0:1900] + "; Message was too long, partly truncated"
    await msg.channel.send(response)


def get_random_from_weighted_table(w_table):
    total_weight = sum([x.weight for x in w_table])
    weight = random.randrange(total_weight)
    for item in w_table:
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
        var_health = (vitality - 10 * tier) * (
            base_hp_per_level - hp_loss_per_tier * tier
        ) + sum([10 * (base_hp_per_level - hp_loss_per_tier * t) for t in range(tier)])
    else:
        var_health = (vitality - 50) * (base_hp_per_level - hp_loss_per_tier * 5) + 800
    return float(var_health)


def roll_gaussian_dist_for_drop(mean: float, std_dev: float) -> float:
    drop_min = max(mean - 3 * std_dev, 1)
    drop_max = mean + 3 * std_dev
    return min(max(normal(mean, std_dev), drop_min), drop_max)


def get_key_for_value(dictionary: dict, value):
    keys = list(dictionary.keys())
    vals = list(dictionary.values())

    position = vals.index(value)
    return keys[position]
