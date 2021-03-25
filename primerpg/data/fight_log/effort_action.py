#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.data.fight_log.action_base import ActionBase
from primerpg.data.fight_log.fight_log import Effort
from primerpg.emojis import skill_emojis, emoji_from_id


class EffortAction(ActionBase):
    def __init__(
        self,
        effort: Effort,
    ):
        super().__init__(False)
        self.effort = effort

    def get_message(self) -> str:
        skill_emoji = skill_emojis[self.effort.skill_id]
        return "(Gained **{}** {} Effort)".format(self.effort.value, emoji_from_id(skill_emoji))
