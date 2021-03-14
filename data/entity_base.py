from abc import abstractmethod
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
from util import calculate_max_hp, get_equipment_stat


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
        phys_atk = self.get_skill_level(strength_skill_id) + self.get_skill_level(
            dexterity_skill_id
        )
        mag_atk = self.get_skill_level(intellect_skill_id) + self.get_skill_level(
            faith_skill_id
        )
        phys_def = self.get_skill_level(defense_skill_id) * 0.75
        mag_def = self.get_skill_level(resistance_skill_id) * 0.75
        aux = (
            self.get_skill_level(speed_skill_id) + self.get_skill_level(luck_skill_id)
        ) * 0.5
        hp = self.get_skill_level(vitality_skill_id) * 0.5
        atk_cb = max(phys_atk, mag_atk) + 0.25 * min(phys_atk, mag_atk)
        def_cb = max(phys_def, mag_def) + 0.25 * min(phys_def, mag_def)
        return floor((atk_cb + def_cb + aux + hp) / 5)

    def get_icon_url(self):
        return self.icon_url

    def get_attack_power(self):
        attack_power = 5.0
        for e in self.equipment:
            attack_power_stat = get_equipment_stat(e.item_id, attack_stat_id)
            if attack_power_stat:
                attack_power += self._apply_scaling(attack_power_stat)

        return floor(attack_power)

    def get_armor_power(self):
        armor_power = 5.0
        for e in self.equipment:
            armor_power_stat = get_equipment_stat(e.item_id, armor_stat_id)
            if armor_power_stat:
                armor_power += self._apply_scaling(armor_power_stat)

        return floor(armor_power)

    def _apply_scaling(self, stat):
        base_value = stat.value
        scaling_values = []
        for skill in self.skills:
            if skill.skill_id in stat.scales_with:
                scaling = stat.scales_with[skill.skill_id]
                scaling_values.append(base_value * scaling * (skill.get_level() / 100))

        return base_value + sum(scaling_values)

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
