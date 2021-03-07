from math import floor


class EntitySkill:
    def __init__(self, entity_id: int, skill_id: int, total_xp: int):
        self.entity_id = entity_id
        self.skill_id = skill_id
        self.total_xp = total_xp
        self.level = self.calculate_level()

    def __repr__(self):
        response = "\nEntity Id: %s" % self.entity_id
        response += "\nSkill Id: %s" % self.skill_id
        response += "\nLevel: %s" % self.total_xp
        response += "\nTotal XP: %s" % self.total_xp
        return response

    def calculate_level(self):
        return floor(self.total_xp / 100)
