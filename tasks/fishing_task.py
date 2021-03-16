import datetime
import random

import util
from consts import base_fish_frequency
from data.item_amount import ItemAmount
from persistence.dto.fish import Fish
from persistence.dto.player_task_core import PlayerTaskCore
from persistence.fish_persistence import get_fish
from tasks.task_base import TaskBase


class FishingTask(TaskBase):
    def __init__(self, task_core: PlayerTaskCore):
        super().__init__(task_core)

    def _calculate_task_rewards(self):
        reward_time = min(
            util.time_since(self.time_started), datetime.timedelta(hours=1)
        )
        start_time_num = int(self.time_started.timestamp())
        total_time_num = int(reward_time.total_seconds())

        self._rewards = []
        if total_time_num < 5:
            return
        for i in range(
            start_time_num + base_fish_frequency,
            start_time_num + total_time_num,
            base_fish_frequency,
        ):
            fish = self.go_fish(i)
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
        return util.get_random_from_weighted_table(fish_table)
