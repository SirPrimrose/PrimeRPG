#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import Optional


class PlayerRank:
    def __init__(self, player_id: int, skill_id: Optional[int], rank: int):
        self.player_id = player_id
        self.skill_id = skill_id
        self.rank = rank

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
