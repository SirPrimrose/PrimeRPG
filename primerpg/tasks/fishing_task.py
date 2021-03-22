#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import datetime
import random

from discord import User

from primerpg import util
from primerpg.data.item_amount import ItemAmount
from primerpg.date_util import time_since
from primerpg.persistence.dto.fish import Fish
from primerpg.persistence.dto.player_task_core import PlayerTaskCore
from primerpg.persistence.fish_persistence import get_fish
from primerpg.tasks.task_base import TaskBase


class FishingTask(TaskBase):
    def __init__(self, task_core: PlayerTaskCore):
        super().__init__(task_core)

    def get_results_string(self, author: User) -> str:
        if len(self.get_task_rewards()) < 1:
            return "{} failed to catch anything!".format(author.name)
        else:
            return "{} caught {} fish!".format(author.name, len(self.get_task_rewards()))

    def _calculate_task_rewards(self) -> None:
        reward_time = min(time_since(self.time_started), datetime.timedelta(seconds=self._get_max_task_seconds()))
        start_time_num = int(self.time_started.timestamp())
        total_time_num = int(reward_time.total_seconds())

        self._rewards = []
        if total_time_num < 5:
            return
        for time in range(
            start_time_num + self.task_frequency,
            start_time_num + total_time_num,
            self.task_frequency,
        ):
            fish = self.go_fish(time)
            if fish:
                self._rewards.append(ItemAmount(fish.item_id, 1))

    def go_fish(self, time: int) -> Fish:
        if random.random() < 0.2:
            if random.random() < 0.2:
                return Fish(0, 0, "Trash", "", "", "", 0)
            else:
                t = datetime.datetime.fromtimestamp(time)
                ig_time = util.get_in_game_time(t)
                ig_weather = util.get_in_game_weather(t)
                return self.get_fish_from_table(ig_time, ig_weather)

    def get_fish_from_table(self, ig_time: str, ig_weather: str) -> Fish:
        fish_table = get_fish(ig_time, ig_weather)
        return util.get_random_from_weighted_list(fish_table)
