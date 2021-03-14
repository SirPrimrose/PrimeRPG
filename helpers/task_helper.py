import datetime

import discord

from consts import fishing_task, mining_task
from data.item_amount import ItemAmount
from helpers import item_helper
from persistence.dto.player_core import gathering_state, idle_state
from persistence.dto.player_task import PlayerTask
from persistence.player_persistence import update_player_data, get_player
from persistence.task_persistence import (
    insert_player_task,
    get_player_task,
    delete_player_task,
)
from tasks.fishing_task import get_fishing_task_rewards
from util import safe_send


async def start_task(msg, player_id, task):
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


async def stop_task(msg, player_id):
    player_data = get_player(player_id)
    if player_data.state == gathering_state:
        # Get task data
        player_data.state = idle_state
        task = get_player_task(player_id)

        update_player_data(player_data)
        delete_player_task(player_id, task.task)

        await get_task_rewards(msg, task)
    else:
        await msg.channel.send(
            "You are not gathering anything.".format(player_data.state)
        )


# TODO Only return the rewards here, show rewards somewhere else
async def get_task_rewards(msg: discord.Message, task: PlayerTask):
    start_time = date_from_str(task.time_started)
    end_time = datetime.datetime.utcnow()
    time_passed = min(end_time - start_time, datetime.timedelta(hours=1))

    rewards = []
    if task.task == fishing_task:
        rewards = get_fishing_task_rewards(start_time, time_passed)
    elif task.task == mining_task:
        print("Mining")

    items = count_items(rewards)
    # TODO Full rewrite of function, use player profile instead of id then save profile
    for item_id, amount in items.items():
        item_helper.give_player_item(task.player_id, ItemAmount(item_id, amount))

    response = "Finished {}. You spent {:.2f} secs collecting.".format(
        task.task, time_passed.total_seconds()
    )
    if len(rewards) > 0:
        response += "\n\nYou earned {}".format(items)
    await safe_send(msg, response)


def count_items(rewards):
    """Reduces the rewards array into a key-value pairing of item ids and the amount of items.

    :param rewards: Array of all rewards, where each reward must have an item id
    :return: Dictionary of amount of items keyed by item id
    """
    items = {}
    for r in rewards:
        if r.item_id in items:
            items[r.item_id] += 1
        else:
            items[r.item_id] = 1
    return items


def str_from_date(date):
    return date.isoformat()


def date_from_str(s):
    return datetime.datetime.fromisoformat(s)
