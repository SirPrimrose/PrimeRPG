import datetime

import discord

from consts import fishing_task, mining_task
from persistence.player_persistence import update_player_data, get_player_data
from persistence.task_persistence import insert_player_task_data, delete_player_task_data, get_player_task_data
from player import gathering_state, idle_state
from task import Task
from tasks.fishing_task import get_fishing_task_rewards
from util import safe_send


async def start_task(msg, player_id, task):
    # TODO Check to make sure a conflicting task is not already started
    player_data = get_player_data(player_id)
    if player_data.state == idle_state:
        player_data.state = gathering_state
        update_player_data(player_data.unique_id, vars(player_data))
        insert_player_task_data(player_id, task, str_from_date(datetime.datetime.utcnow()))
        await msg.channel.send('Started {0}.'.format(task))
    else:
        await msg.channel.send('You are busy {0}.'.format(player_data.state))


async def stop_task(msg, player_id):
    player_data = get_player_data(player_id)
    if player_data.state == gathering_state:
        # Get task data
        player_data.state = idle_state
        task_data = get_player_task_data(player_id)
        task = Task(task_data[1], task_data[2])

        update_player_data(player_data.unique_id, vars(player_data))
        delete_player_task_data(player_id, task.task)

        await get_task_rewards(msg, task)
    else:
        await msg.channel.send('You are not gathering anything.'.format(player_data.state))


async def get_task_rewards(msg: discord.Message, task: Task):
    start_time = date_from_str(task.time_started)
    end_time = datetime.datetime.utcnow()
    time_passed = min(end_time - start_time, datetime.timedelta(hours=1))

    rewards = []
    if task.task == fishing_task:
        rewards = get_fishing_task_rewards(start_time, time_passed)
    elif task.task == mining_task:
        print('Mining')

    response = 'Finished {}. You spent {:.2f} secs collecting.'.format(task.task, time_passed.total_seconds())
    if len(rewards) > 0:
        response += '\n\nYou earned {}'.format(rewards)
    await safe_send(msg, response)


def str_from_date(date):
    return date.isoformat()


def date_from_str(s):
    return datetime.datetime.fromisoformat(s)
