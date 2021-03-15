import datetime
from typing import List, Dict

from consts import fishing_task, mining_task
from data.item_amount import ItemAmount
from data.player_profile import PlayerProfile
from helpers import item_helper
from helpers.player_helper import save_player_profile
from persistence.dto.player_core import gathering_state, idle_state
from persistence.dto.player_task import PlayerTask
from persistence.player_persistence import update_player_data, get_player
from persistence.task_persistence import (
    insert_player_task,
    delete_player_task,
)
from tasks.fishing_task import get_fishing_task_rewards


async def handle_start_task(msg, player_id, task):
    player_data = get_player(player_id)
    if player_data.state == idle_state:
        player_data.state = gathering_state
        update_player_data(player_data)
        insert_player_task(
            PlayerTask(player_id, task, str_from_date(datetime.datetime.utcnow()))
        )
        await msg.channel.send("Started {0}.".format(task))
    else:
        await msg.channel.send("You are busy {0}.".format(player_data.state))


def handle_stop_task(
    msg, profile: PlayerProfile, task: PlayerTask
) -> (List[ItemAmount], datetime.timedelta):
    if profile.core.state == gathering_state:
        if task:
            profile.core.state = idle_state
            delete_player_task(profile.core.unique_id, task.task)

            rewards, time_passed = get_task_rewards(task)

            for item in rewards:
                item_helper.give_player_item(profile, item)
            save_player_profile(profile)

            return rewards, time_passed
        else:
            profile.core.state = idle_state
            save_player_profile(profile)
            return None, None


def get_task_rewards(task: PlayerTask) -> (List[ItemAmount], datetime.timedelta):
    start_time = date_from_str(task.time_started)
    end_time = datetime.datetime.utcnow()
    time_passed = min(end_time - start_time, datetime.timedelta(hours=1))

    rewards = []
    if task.task == fishing_task:
        rewards = get_fishing_task_rewards(start_time, time_passed)
    elif task.task == mining_task:
        print("Mining")

    return count_items(rewards), time_passed


def count_items(rewards) -> List[ItemAmount]:
    """Reduces the rewards array into a key-value pairing of item ids and the amount of items.

    :param rewards: Array of all rewards, where each reward must have an item id
    :return: Dictionary of amount of items keyed by item id
    """
    items: Dict[int, ItemAmount] = dict()
    for r in rewards:
        if r.item_id in items:
            items[r.item_id].quantity += r.quantity
        else:
            items[r.item_id] = ItemAmount(r.item_id, r.quantity)
    return list(items.values())


def str_from_date(date):
    return date.isoformat()


def date_from_str(s):
    return datetime.datetime.fromisoformat(s)
