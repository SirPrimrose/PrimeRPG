class PlayerEquipment:
    def __init__(self, player_id, equipment_slot_id, item_id):
        self.player_id = player_id
        self.equipment_slot_id = equipment_slot_id
        self.item_id = item_id

    def __repr__(self):
        response = "Player Id: %s" % self.player_id
        response += "\nEquipment Slot Id: %s" % self.equipment_slot_id
        response += "\nItem Id: %s" % self.item_id
        return response
