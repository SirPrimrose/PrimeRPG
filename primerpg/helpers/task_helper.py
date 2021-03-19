#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import datetime
from typing import Type, Optional

from primerpg.consts import fishing_task_id
from primerpg.data.player_profile import PlayerProfile
from primerpg.date_util import str_from_date
from primerpg.helpers import item_helper
from primerpg.helpers.player_helper import save_player_profile
from primerpg.helpers.state_helper import idle_state_id, gathering_state_id
from primerpg.persistence.dto.player_task_core import PlayerTaskCore
from primerpg.persistence.player_persistence import update_player_data, get_player
from primerpg.persistence.player_task_persistence import insert_player_task, delete_player_task, get_player_task
from primerpg.tasks.fishing_task import FishingTask
from primerpg.tasks.task_base import TaskBase

task_dict = {fishing_task_id: FishingTask}


def handle_start_task(player_id: int, task_id: int) -> TaskBase:
    player_data = get_player(player_id)
    player_data.state_id = gathering_state_id
    update_player_data(player_data)
    task_core = PlayerTaskCore(player_id, task_id, str_from_date(datetime.datetime.utcnow()))
    insert_player_task(task_core)
    return get_task_for_id(task_core.task_id)(task_core)


def handle_collect_task(profile: PlayerProfile) -> TaskBase:
    profile.core.state_id = idle_state_id
    task = get_current_player_task(profile.core.unique_id)

    for item in task.get_task_rewards():
        item_helper.give_player_item(profile, item)

    delete_player_task(profile.core.unique_id, task.task_id)
    save_player_profile(profile)

    return task


def get_current_player_task(player_id: int) -> Optional[TaskBase]:
    task_core = get_player_task(player_id)
    if task_core:
        return get_task_for_id(task_core.task_id)(task_core)
    else:
        return None


def get_task_for_id(task_id: int) -> Type[TaskBase]:
    if task_id in task_dict:
        return task_dict[task_id]
    else:
        return TaskBase
