import datetime

from persistence.player_persistence import update_player_data, get_player_data
from persistence.task_persistence import insert_player_task_data, delete_player_task_data, get_player_task_data
from player import gathering_state, idle_state
from task import Task


async def start_task(msg, player_id, task):
    # TODO Check to make sure a conflicting task is not already started
    datetime.datetime.now()
    player_data = get_player_data(player_id)
    if player_data.state == idle_state:
        player_data.state = gathering_state
        update_player_data(player_data.unique_id, vars(player_data))
        insert_player_task_data(player_id, task, str_from_date(now()))
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

        # Calculate time passed and run rewards for task type
        start_time = date_from_str(task.time_started)
        end_time = now()
        time_passed = min(end_time - start_time, datetime.timedelta(hours=1))
        await msg.channel.send('Collected things. You spent {:.2f} secs collecting.'
                               .format(time_passed.total_seconds()))
    else:
        await msg.channel.send('You are not gathering anything.'.format(player_data.state))


def now():
    return datetime.datetime.utcnow()


def str_from_date(date):
    return date.isoformat()


def date_from_str(s):
    return datetime.datetime.fromisoformat(s)
