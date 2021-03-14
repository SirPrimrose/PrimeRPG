from copy import copy
from typing import List

from data.fight_log.action_base import ActionBase
from data.item_amount import ItemAmount


class Effort(object):
    def __init__(self, skill_id: int, value: int):
        self.skill_id = skill_id
        self.value = value


class FightLog:
    def __init__(self):
        self.actions: List[ActionBase] = []
        self.efforts: List[Effort] = []
        self._rewards: List[ItemAmount] = []

    def add_action(self, action: ActionBase):
        self.actions.append(action)

    def add_effort(self, effort: Effort):
        for e in self.efforts:
            if e.skill_id == effort.skill_id:
                e.value += effort.value
                return
        self.efforts.append(copy(effort))

    def add_rewards(self, rewards: List[ItemAmount]):
        self._rewards.extend(rewards)

    def get_rewards(self):
        return self._rewards
