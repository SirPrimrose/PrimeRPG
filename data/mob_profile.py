from consts import strength_skill_id, vitality_skill_id
from data.entity_base import EntityBase


class MobProfile(EntityBase):
    def __init__(self, *args):
        super(EntityBase, self).__init__(args)

    def get_attack_power(self):
        return self.get_skill_value(strength_skill_id) * 10

    def get_armor_power(self):
        return self.get_skill_value(vitality_skill_id) * 10
