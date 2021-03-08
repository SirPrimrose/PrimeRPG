from typing import List

from consts import attack_stat_id, armor_stat_id
from data.entity_base import EntityBase
from data.player_core import PlayerCore
from data.player_equipment import PlayerEquipment
from data.player_skill import PlayerSkill
from persistence.equipment_stat_persistence import get_equipment_stat


class PlayerProfile(EntityBase):
    def __init__(
        self,
        core: PlayerCore,
        skills: List[PlayerSkill],
        equipment: List[PlayerEquipment],
    ):
        super().__init__(core.current_hp, core.name, skills)
        self.core = core
        self.equipment = equipment

    def __repr__(self):
        response = super.__repr__()
        response += "\nCore: \n%s" % self.core
        response += "\nEquipment: \n%s" % self.equipment
        return response

    def get_attack_power(self):
        attack_power = 10
        for e in self.equipment:
            attack_power_stat = get_equipment_stat(e.item_id, attack_stat_id)
            attack_power += self.apply_scaling(attack_power_stat)

        return attack_power

    def get_armor_power(self):
        armor_power = 10
        for e in self.equipment:
            armor_power_stat = get_equipment_stat(e.item_id, armor_stat_id)
            armor_power += self.apply_scaling(armor_power_stat)

        return armor_power

    def apply_scaling(self, stat):
        base_value = stat.value
        scaling_values = []
        for skill in self.skills:
            if skill.skill_id in stat.scales_with:
                scaling = stat.scales_with[skill.skill_id]
                scaling_values.append(base_value * scaling * (skill.level / 100))

        return base_value + sum(scaling_values)
