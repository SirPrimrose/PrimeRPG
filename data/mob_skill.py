from data.skill import EntitySkill


class MobSkill(EntitySkill):
    def __init__(self, mob_id: int, skill_id: int, total_xp: int):
        super().__init__(mob_id, skill_id, total_xp)

    def get_mob_id(self):
        return self.entity_id
