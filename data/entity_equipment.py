class EntityEquipment:
    def __init__(self, entity_id, equipment_slot_id, item_id):
        self.entity_id = entity_id
        self.equipment_slot_id = equipment_slot_id
        self.item_id = item_id

    def __repr__(self):
        response = "Entity ID: %s" % self.entity_id
        response += "\nEquipment Slot ID: %s" % self.equipment_slot_id
        response += "\nItem ID: %s" % self.item_id
        return response
