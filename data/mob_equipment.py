class MobEquipment:
    def __init__(self, mob_id, equipment_slot_id, item_id):
        self.mob_id = mob_id
        self.equipment_slot_id = equipment_slot_id
        self.item_id = item_id

    def __repr__(self):
        response = "Mob ID: %s" % self.mob_id
        response += "\nEquipment Slot ID: %s" % self.equipment_slot_id
        response += "\nItem ID: %s" % self.item_id
        return response
