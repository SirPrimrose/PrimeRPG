class PlayerSkill:
    def __init__(self, player_id: int, skill_id: int, total_xp: int):
        self.player_id = player_id
        self.skill_id = skill_id
        self.total_xp = total_xp

    def __repr__(self):
        response = "Player Id: %s" % self.player_id
        response += "\nSkill Id: %s" % self.skill_id
        response += "\nTotal XP: %s" % self.total_xp
        return response
