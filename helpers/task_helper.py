import datetime
from typing import Type

from consts import fishing_task_id
from data.player_profile import PlayerProfile
from date_util import str_from_date
from helpers import item_helper
from helpers.player_helper import save_player_profile
from persistence.dto.player_core import gathering_state, idle_state
from persistence.dto.player_task_core import PlayerTaskCore
from persistence.player_persistence import update_player_data, get_player
from persistence.player_task_persistence import (
    insert_player_task,
    delete_player_task,
)
from tasks.fishing_task import FishingTask
from tasks.task_base import TaskBase

task_dict = {fishing_task_id: FishingTask}


def handle_start_task(player_id: int, task_id: int):
    player_data = get_player(player_id)
    if player_data.state == idle_state:
        player_data.state = gathering_state
        update_player_data(player_data)
        insert_player_task(
            PlayerTaskCore(
                player_id, task_id, str_from_date(datetime.datetime.utcnow())
            )
        )


def handle_collect(profile: PlayerProfile, task_core: PlayerTaskCore) -> TaskBase:
    if profile.core.state == gathering_state:
        profile.core.state = idle_state
        task = get_task_for_id(task_core.task_id)(task_core)

        for item in task.get_task_rewards():
            item_helper.give_player_item(profile, item)

        delete_player_task(profile.core.unique_id, task_core.task_id)
        save_player_profile(profile)

        return task


def get_task_for_id(task_id: int) -> Type[TaskBase]:
    if task_id in task_dict:
        return task_dict[task_id]
    else:
        return TaskBase
