from data.entity_equipment import EntityEquipment


class PlayerEquipment(EntityEquipment):
    def __init__(self, entity_id, equipment_slot_id, item_id):
        super().__init__(entity_id, equipment_slot_id, item_id)

    def get_player_id(self):
        return self.entity_id
