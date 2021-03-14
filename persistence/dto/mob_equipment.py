from data.entity_equipment import EntityEquipment


class MobEquipment(EntityEquipment):
    def __init__(self, mob_id, equipment_slot_id, item_id):
        super().__init__(mob_id, equipment_slot_id, item_id)

    def get_mob_id(self):
        return self.entity_id
