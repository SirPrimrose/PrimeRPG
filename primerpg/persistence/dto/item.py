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
    ):
        self.unique_id = unique_id
        self.item_category_id = item_category_id
        self.equipment_category_id = equipment_category_id
        self.name = name
        self.value = value

    def __repr__(self):
        response = "Unique Id: %s" % self.unique_id
        response += "\nItem Category Id: %s" % self.item_category_id
        response += "\nEquipment Category Id: %s" % self.equipment_category_id
        response += "\nName: %s" % self.name
        response += "\nValue: %s" % self.value
        return response
