#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class EntityEquipment:
    def __init__(self, entity_id, equipment_category_id, item_id):
        self.entity_id = entity_id
        self.equipment_category_id = equipment_category_id
        self.item_id = item_id

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
