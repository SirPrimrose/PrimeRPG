#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class EntityEquipment:
    def __init__(self, entity_id, equipment_category_id, item_id):
        self.entity_id = entity_id
        self.equipment_category_id = equipment_category_id
        self.item_id = item_id

    def __repr__(self):
        response = "Entity ID: %s" % self.entity_id
        response += "\nEquipment Category ID: %s" % self.equipment_category_id
        response += "\nItem ID: %s" % self.item_id
        return response
