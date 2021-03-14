from data.entity_equipment import EntityEquipment


class PlayerEquipment(EntityEquipment):
    def __init__(self, player_id, equipment_category_id, item_id):
        super().__init__(player_id, equipment_category_id, item_id)

    def get_player_id(self):
        return self.entity_id