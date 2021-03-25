#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List


class CommandRequirement:
    def __init__(self, unique_id: int, name: str, zone_id: int, cooldown: int, allowed_state_ids: List[int]):
        self.unique_id = unique_id
        self.name = name
        self.zone_id = zone_id
        self.cooldown = cooldown
        self.allowed_state_ids = allowed_state_ids

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
