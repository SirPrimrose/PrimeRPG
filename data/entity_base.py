from math import floor
from typing import List

from consts import (
    vitality_skill_id,
    strength_skill_id,
    dexterity_skill_id,
    intellect_skill_id,
    resistance_skill_id,
    faith_skill_id,
    speed_skill_id,
    luck_skill_id,
    defense_skill_id,
    attack_stat_id,
    armor_stat_id,
)
from data.entity_equipment import EntityEquipment
from data.entity_skill import EntitySkill
from persistence.equipment_stat_persistence import get_equipment_stat


class EntityBase:
    def __init__(
        self,
        name: str,
        icon_url: str,
        skills: List[EntitySkill],
        equipment: List[EntityEquipment],
        current_hp: int = None,
    ):
        self.name = name
        self.icon_url = icon_url
        self.skills = skills
        self.equipment = equipment
        self.current_hp = current_hp

    def __repr__(self):
        response = "Current HP: %s" % self.current_hp
        response += "\nName: %s" % self.name
        response += "\nSkills: %s" % self.skills
        return response

    def get_skill_level(self, skill_id) -> int:
        try:
            result = next(filter(lambda skill: skill.skill_id == skill_id, self.skills))
        except StopIteration:
            result = None
        return 0 if not result else result.level

    def is_dead(self):
        return self.current_hp <= 0

    def get_max_hp(self):
        return self.get_skill_level(vitality_skill_id) * 10

    def get_combat_level(self):
        phys_atk = self.get_skill_level(strength_skill_id) + self.get_skill_level(
            dexterity_skill_id
        )
        mag_atk = self.get_skill_level(intellect_skill_id) + self.get_skill_level(
            faith_skill_id
        )
        phys_def = self.get_skill_level(defense_skill_id)
        mag_def = self.get_skill_level(resistance_skill_id)
        aux = self.get_skill_level(speed_skill_id) + self.get_skill_level(luck_skill_id)
        hp = self.get_skill_level(vitality_skill_id)
        atk_cb = max(phys_atk, mag_atk) + 0.25 * min(phys_atk, mag_atk)
        def_cb = max(phys_def, mag_def) + 0.25 * min(phys_def, mag_def)
        return floor((atk_cb + def_cb + aux + hp) / 5)

    def get_icon_url(self):
        return self.icon_url

    def get_attack_power(self):
        attack_power = 10
        for e in self.equipment:
            # TODO Preload this data so it isn't fetched from the database
            attack_power_stat = get_equipment_stat(e.item_id, attack_stat_id)
            if attack_power_stat:
                attack_power += self.apply_scaling(attack_power_stat)

        return attack_power

    def get_armor_power(self):
        armor_power = 10
        for e in self.equipment:
            armor_power_stat = get_equipment_stat(e.item_id, armor_stat_id)
            if armor_power_stat:
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
