#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from copy import copy
from typing import List

from primerpg.data.fight_log.action_base import ActionBase
from primerpg.data.item_amount import ItemAmount


class Effort(object):
    def __init__(self, skill_id: int, value: int):
        self.skill_id = skill_id
        self.value = value


class FightLog:
    def __init__(self):
        self.actions: List[ActionBase] = []
        self._efforts: List[Effort] = []
        self._rewards: List[ItemAmount] = []

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)

    def add_action(self, action: ActionBase):
        self.actions.append(action)

    def add_effort(self, effort: Effort):
        for e in self._efforts:
            if e.skill_id == effort.skill_id:
                e.value += effort.value
                return
        self._efforts.append(copy(effort))

    def get_efforts(self):
        return self._efforts

    def add_rewards(self, rewards: List[ItemAmount]):
        self._rewards.extend(rewards)

    def get_rewards(self):
        return self._rewards

    def get_last_actions(self, num_of_actions: int) -> List[ActionBase]:
        actions_to_show = min(num_of_actions, len(self.actions))
        return self.actions[-actions_to_show:]
