#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class BossCore:
    def __init__(self, mob_id: int, zone_id: int, type_strengths: list[int], type_weaknesses: list[int]):
        self.mob_id = mob_id
        self.zone_id = zone_id
        self.type_strength_ids = type_strengths
        self.type_weakness_ids = type_weaknesses

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
