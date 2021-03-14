from data.entity_skill import EntitySkill


class PlayerSkill(EntitySkill):
    def __init__(self, player_id: int, skill_id: int, total_xp: int):
        super().__init__(player_id, skill_id, total_xp)

    def get_player_id(self):
        return self.entity_id
