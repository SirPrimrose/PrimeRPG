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
        usage_effects: list[dict],
    ):
        self.unique_id = unique_id
        self.item_category_id = item_category_id
        self.equipment_category_id = equipment_category_id
        self.name = name
        self.value = value
        self.shop_zone_id = shop_zone_id
        self.usage_effects = usage_effects

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nItem Category Id: %s" % self.item_category_id
        response += "\nEquipment Category Id: %s" % self.equipment_category_id
        response += "\nName: %s" % self.name
        response += "\nValue: %s" % self.value
        response += "\nshop_zone_id: %s" % self.shop_zone_id
        response += "\nusage_effects: %s" % self.usage_effects
        return response
