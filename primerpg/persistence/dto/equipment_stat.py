#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class EquipmentStat:
    def __init__(
        self,
        item_id: int,
        equipment_stat_category_id: int,
        value: int,
        scales_with: dict,
    ):
        self.item_id = item_id
        self.equipment_stat_category_id = equipment_stat_category_id
        self.value = value
        self.scales_with = scales_with

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
