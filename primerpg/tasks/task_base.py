#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from abc import abstractmethod
from typing import List, Dict

from primerpg.data.item_amount import ItemAmount
from primerpg.date_util import date_from_str
from primerpg.persistence.dto.player_task_core import PlayerTaskCore


class TaskBase:
    def __init__(self, task_core: PlayerTaskCore):
        self.player_id = task_core.player_id
        self.task_id = task_core.task_id
        self.time_started = date_from_str(task_core.time_started)
        self._rewards: List[ItemAmount] = []
        self._calculate_task_rewards()
        self._collect_rewards()

    @abstractmethod
    def _calculate_task_rewards(self):
        pass

    def get_task_rewards(self) -> List[ItemAmount]:
        return self._rewards

    def _collect_rewards(self):
        """Reduces the rewards list by combining similar item id entries into a single ItemAmount."""
        items: Dict[int, ItemAmount] = dict()
        for r in self._rewards:
            if r.item_id in items:
                items[r.item_id].quantity += r.quantity
            else:
                items[r.item_id] = ItemAmount(r.item_id, r.quantity)
        self._rewards = list(items.values())
