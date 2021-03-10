from data.fight_log.action_base import ActionBase
from emojis import turn_emoji


class TurnAction(ActionBase):
    def __init__(self, turn_number: int, *args):
        super(ActionBase, self).__init__(*args)
        self.turn_number = turn_number

    def get_message(self):
        return "{0} {1}".format(
            turn_emoji,
            self.turn_number,
        )
