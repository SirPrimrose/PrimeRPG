from abc import abstractmethod
from math import floor
from typing import List

from consts import (
    health_skill_id,
    strength_skill_id,
    dexterity_skill_id,
    intellect_skill_id,
    resistance_skill_id,
    faith_skill_id,
    speed_skill_id,
    luck_skill_id,
    defense_skill_id,
)
from data.skill import EntitySkill


class EntityBase:
    def __init__(
        self, current_hp: int, name: str, icon_url: str, skills: List[EntitySkill]
    ):
        self.current_hp = current_hp
        self.name = name
        self.icon_url = icon_url
        self.skills = skills

    def __repr__(self):
        response = "Current HP: %s" % self.current_hp
        response += "\nName: %s" % self.name
        response += "\nSkills: %s" % self.skills
        return response

    def get_skill_value(self, skill_id):
        result = next(filter(lambda skill: skill.skill_id == skill_id, self.skills))
        return result if result else 0

    def is_dead(self):
        return self.current_hp <= 0

    def get_max_hp(self):
        return self.get_skill_value(health_skill_id).level * 10

    def get_combat_level(self):
        phys_atk = (
            self.get_skill_value(strength_skill_id).level
            + self.get_skill_value(dexterity_skill_id).level
        )
        mag_atk = (
            self.get_skill_value(intellect_skill_id).level
            + self.get_skill_value(faith_skill_id).level
        )
        phys_def = self.get_skill_value(defense_skill_id).level
        mag_def = self.get_skill_value(resistance_skill_id).level
        aux = (
            self.get_skill_value(speed_skill_id).level
            + self.get_skill_value(luck_skill_id).level
        )
        hp = self.get_skill_value(health_skill_id).level
        atk_cb = max(phys_atk, mag_atk) + 0.25 * min(phys_atk, mag_atk)
        def_cb = max(phys_def, mag_def) + 0.25 * min(phys_def, mag_def)
        return floor((atk_cb + def_cb + aux + hp) / 5)

    def get_icon_url(self):
        return self.icon_url

    @abstractmethod
    def get_attack_power(self):
        pass

    @abstractmethod
    def get_armor_power(self):
        pass
