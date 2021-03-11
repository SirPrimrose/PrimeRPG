from data.entity_equipment import EntityEquipment


class PlayerEquipment(EntityEquipment):
    def __init__(self, *args):
        super().__init__(*args)

    def get_player_id(self):
        return self.entity_id
