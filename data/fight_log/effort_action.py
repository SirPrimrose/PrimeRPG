from data.fight_log.action_base import ActionBase
from data.fight_log.fight_log import Effort
from emojis import skill_emojis


class EffortAction(ActionBase):
    def __init__(
        self,
        effort: Effort,
    ):
        super().__init__(False)
        self.effort = effort

    def get_message(self):
        keys = list(skill_emojis.keys())
        vals = list(skill_emojis.values())

        position = vals.index(self.effort.skill_id)
        skill_emoji = keys[position]
        return "(Gained **{}** {} Effort)".format(self.effort.value, skill_emoji)
