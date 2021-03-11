from data.entity_equipment import EntityEquipment


class MobEquipment(EntityEquipment):
    def __init__(self, *args):
        super().__init__(*args)

    def get_mob_id(self):
        return self.entity_id
