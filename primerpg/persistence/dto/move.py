#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class Move:
    def __init__(
        self,
        unique_id: int,
        power: int,
        hits: int,
        damage_type_id: int,
        scaling_equipment_stat_id: int,
        armor_equipment_stat_id: int,
        success_chance: float,
        name: str,
    ):
        self.unique_id = unique_id
        self.power = power
        self.hits = hits
        self.damage_type_id = damage_type_id
        self.scaling_equipment_stat_id = scaling_equipment_stat_id
        self.armor_equipment_stat_id = armor_equipment_stat_id
        self.success_chance = success_chance
        self.name = name

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
