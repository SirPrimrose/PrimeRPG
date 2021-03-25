#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class Item:
    def __init__(
        self,
        unique_id: int,
        item_category_id: int,
        equipment_category_id: int,
        name: str,
        value: int,
        shop_zone_id: int,
        moveset_ids: list[int],
        usage_effects: list[dict],
    ):
        self.unique_id = unique_id
        self.item_category_id = item_category_id
        self.equipment_category_id = equipment_category_id
        self.name = name
        self.value = value
        self.shop_zone_id = shop_zone_id
        self.moveset_ids = moveset_ids
        self.usage_effects = usage_effects

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
