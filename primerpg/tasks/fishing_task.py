#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import datetime
import random
from math import floor

from primerpg import util
from primerpg.data.item_amount import ItemAmount
from primerpg.persistence.dto.fish import Fish
from primerpg.persistence.dto.player_task_core import PlayerTaskCore
from primerpg.persistence.fish_persistence import get_fish
from primerpg.tasks.task_base import TaskBase

base_fish_frequency = 60  # seconds


class FishingTask(TaskBase):
    def __init__(self, task_core: PlayerTaskCore):
        super().__init__(task_core)

    def _calculate_task_rewards(self):
        reward_time = min(util.time_since(self.time_started), datetime.timedelta(seconds=self._get_max_task_seconds()))
        start_time_num = int(self.time_started.timestamp())
        total_time_num = int(reward_time.total_seconds())

        self._rewards = []
        if total_time_num < 5:
            return
        for time in range(
            start_time_num + base_fish_frequency,
            start_time_num + total_time_num,
            base_fish_frequency,
        ):
            fish = self.go_fish(time)
            if fish:
                self._rewards.append(ItemAmount(fish.item_id, 1))

    def get_task_attempt_count(self) -> int:
        reward_time = min(util.time_since(self.time_started), datetime.timedelta(seconds=self._get_max_task_seconds()))
        total_time_num = int(reward_time.total_seconds())
        return floor(total_time_num / base_fish_frequency)

    def get_current_attempt_progress(self) -> float:
        reward_time = min(util.time_since(self.time_started), datetime.timedelta(seconds=self._get_max_task_seconds()))
        total_time_num = int(reward_time.total_seconds())
        return (total_time_num - self.get_task_attempt_count() * base_fish_frequency) / base_fish_frequency

    def get_max_task_attempts(self) -> int:
        return floor(self._get_max_task_seconds() / base_fish_frequency)

    def _get_max_task_seconds(self) -> int:
        return 3600

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
        return util.get_random_from_weighted_table(fish_table)
