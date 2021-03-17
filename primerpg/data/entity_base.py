from abc import abstractmethod
from math import floor
from typing import List

from primerpg.consts import (
    vitality_skill_id,
    strength_skill_id,
    dexterity_skill_id,
    intellect_skill_id,
    resistance_skill_id,
    faith_skill_id,
    speed_skill_id,
    luck_skill_id,
    defense_skill_id,
    physical_attack_stat_id,
    magical_armor_stat_id,
    magical_attack_stat_id,
    physical_armor_stat_id,
)
from primerpg.data.entity_equipment import EntityEquipment
from primerpg.data.entity_skill import EntitySkill
from primerpg.helpers.stat_helper import get_total_scaled_stat_value
from primerpg.util import calculate_max_hp


class EntityBase:
    def __init__(
        self,
        name: str,
        icon_url: str,
        skills: List[EntitySkill],
        equipment: List[EntityEquipment],
    ):
        self.name = name
        self.icon_url = icon_url
        self.skills = skills
        self.equipment = equipment

    def __repr__(self):
        response = "Current HP: %s" % self.get_current_hp()
        response += "\nName: %s" % self.name
        response += "\nSkills: %s" % self.skills
        return response

    @abstractmethod
    def get_current_hp(self) -> float:
        pass

    @abstractmethod
    def set_current_hp(self, new_hp: float) -> None:
        pass

    def change_current_hp(self, hp_delta: float):
        new_hp = min(max(self.get_current_hp() + hp_delta, 0), self.get_max_hp())
        self.set_current_hp(new_hp)

    def get_skill_level(self, skill_id) -> int:
        try:
            result = next(filter(lambda skill: skill.skill_id == skill_id, self.skills))
        except StopIteration:
            result = None
        return 0 if not result else result.get_level()

    def is_dead(self):
        return self.get_current_hp() <= 0

    def get_max_hp(self) -> float:
        vitality = self.get_skill_level(vitality_skill_id)
        return calculate_max_hp(vitality)

    def get_combat_level(self):
        phys_atk = self.get_skill_level(strength_skill_id) + self.get_skill_level(dexterity_skill_id)
        mag_atk = self.get_skill_level(intellect_skill_id) + self.get_skill_level(faith_skill_id)
        phys_def = self.get_skill_level(defense_skill_id) * 0.75
        mag_def = self.get_skill_level(resistance_skill_id) * 0.75
        aux = (self.get_skill_level(speed_skill_id) + self.get_skill_level(luck_skill_id)) * 0.5
        hp = self.get_skill_level(vitality_skill_id) * 0.5
        atk_cb = max(phys_atk, mag_atk) + 0.25 * min(phys_atk, mag_atk)
        def_cb = max(phys_def, mag_def) + 0.25 * min(phys_def, mag_def)
        return floor((atk_cb + def_cb + aux + hp) / 5)

    def get_icon_url(self):
        return self.icon_url

    def get_phys_atk_power(self) -> float:
        return get_total_scaled_stat_value(physical_attack_stat_id, self.skills, self.equipment)

    def get_phys_arm_power(self) -> float:
        return get_total_scaled_stat_value(physical_armor_stat_id, self.skills, self.equipment)

    def get_mag_atk_power(self) -> float:
        return get_total_scaled_stat_value(magical_attack_stat_id, self.skills, self.equipment)

    def get_mag_arm_power(self) -> float:
        return get_total_scaled_stat_value(magical_armor_stat_id, self.skills, self.equipment)

    def give_skill_effort(self, skill_id: int, value: int):
        if value < 0:
            return
        try:
            result = next(filter(lambda skill: skill.skill_id == skill_id, self.skills))
            result.modify_xp(value)
        except StopIteration:
            pass

    def get_equipment(self, equipment_category_id) -> EntityEquipment:
        try:
            result = next(
                filter(
                    lambda equip: equip.equipment_category_id == equipment_category_id,
                    self.equipment,
                )
            )
        except StopIteration:
            result = None
        return result
