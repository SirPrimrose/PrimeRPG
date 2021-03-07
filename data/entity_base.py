from abc import abstractmethod
from typing import List

from data.skill import EntitySkill


class EntityBase:
    def __init__(self, current_hp: int, name: str, skills: List[EntitySkill]):
        self.current_hp = current_hp
        self.name = name
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

    @abstractmethod
    def get_attack_power(self):
        pass

    @abstractmethod
    def get_defense_power(self):
        pass
