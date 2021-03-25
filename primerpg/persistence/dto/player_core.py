#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class PlayerCore:
    def __init__(
        self,
        unique_id: int,
        name: str,
        avatar_url: str,
        state_id: int,
        zone_id: int,
        current_hp: float,
        hp_regen: float,
    ):
        self.unique_id = unique_id
        self.name = name
        self.avatar_url = avatar_url
        self.state_id = state_id
        self.zone_id = zone_id
        self.current_hp = current_hp
        self.hp_regen = hp_regen

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
