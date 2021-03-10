from typing import List

from data.fight_log.action_base import ActionBase


class FightLog:
    def __init__(self):
        self.actions: List[ActionBase] = []

    def add_action(self, action: ActionBase):
        self.actions.append(action)
