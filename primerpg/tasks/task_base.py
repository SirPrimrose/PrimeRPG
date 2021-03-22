#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
import datetime
from abc import abstractmethod
from math import floor
from typing import List, Dict

from discord import User

from primerpg.data.item_amount import ItemAmount
from primerpg.data_cache import get_task_category_name
from primerpg.date_util import date_from_str
from primerpg.persistence.dto.player_task_core import PlayerTaskCore
from primerpg.date_util import time_since


class TaskBase:
    def __init__(self, task_core: PlayerTaskCore):
        self.player_id = task_core.player_id
        self.task_id = task_core.task_id
        self.time_started = date_from_str(task_core.time_started)
        self.task_name = get_task_category_name(task_core.task_id)
        self.task_frequency = 60  # seconds
        self._rewards: List[ItemAmount] = []
        self._calculate_task_rewards()
        self._reduce_rewards()

    @abstractmethod
    def get_results_string(self, author: User) -> str:
        pass

    @abstractmethod
    def _calculate_task_rewards(self) -> None:
        pass

    def get_task_attempt_count(self) -> int:
        total_time_num = self._get_total_reward_seconds()
        return floor(total_time_num / self.task_frequency)

    def get_current_attempt_progress(self) -> float:
        total_time_num = self._get_total_reward_seconds()
        return (total_time_num / self.task_frequency) - self.get_task_attempt_count()

    def get_max_task_attempts(self) -> int:
        return floor(self._get_max_task_seconds() / self.task_frequency)

    def _get_max_task_seconds(self) -> int:
        return 3600

    def _get_total_reward_seconds(self) -> int:
        reward_time = min(time_since(self.time_started), datetime.timedelta(seconds=self._get_max_task_seconds()))
        return int(reward_time.total_seconds())

    def get_task_rewards(self) -> List[ItemAmount]:
        return self._rewards

    def _reduce_rewards(self):
        """Reduces the rewards list by combining similar item id entries into a single ItemAmount."""
        items: Dict[int, ItemAmount] = dict()
        for r in self._rewards:
            if r.item_id in items:
                items[r.item_id].quantity += r.quantity
            else:
                items[r.item_id] = ItemAmount(r.item_id, r.quantity)
        self._rewards = list(items.values())
