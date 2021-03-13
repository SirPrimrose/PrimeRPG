from data.fight_log.action_base import ActionBase
from data.fight_log.fight_log import Effort
from emojis import skill_emojis
from util import get_key_for_value


class EffortAction(ActionBase):
    def __init__(
        self,
        effort: Effort,
    ):
        super().__init__(False)
        self.effort = effort

    def get_message(self):
        skill_emoji = get_key_for_value(skill_emojis, self.effort.skill_id)
        return "(Gained **{}** {} Effort)".format(self.effort.value, skill_emoji)
