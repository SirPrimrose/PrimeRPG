from primerpg.data.fight_log.action_base import ActionBase
from primerpg.emojis import turn_emoji


class TurnAction(ActionBase):
    def __init__(self, turn_number: int):
        super().__init__()
        self.turn_number = turn_number

    def get_message(self):
        return "{0} {1}".format(
            turn_emoji,
            self.turn_number,
        )
