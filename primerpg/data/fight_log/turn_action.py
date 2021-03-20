#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.data.fight_log.action_base import ActionBase
from primerpg.emojis import turn_emoji_id, emoji_from_id


class TurnAction(ActionBase):
    def __init__(self, turn_number: int):
        super().__init__()
        self.turn_number = turn_number

    def get_message(self):
        return "{0} {1}".format(
            emoji_from_id(turn_emoji_id),
            self.turn_number,
        )
