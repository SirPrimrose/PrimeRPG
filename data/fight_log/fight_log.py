from typing import List

from data.fight_log.action_base import ActionBase


class Effort(object):
    def __init__(self, skill_id: int, value: int):
        self.skill_id = skill_id
        self.value = value


class FightLog:
    def __init__(self):
        self.actions: List[ActionBase] = []
        self.efforts: List[Effort] = []

    def add_action(self, action: ActionBase):
        self.actions.append(action)

    def add_effort(self, effort: Effort):
        self.efforts.append(effort)
