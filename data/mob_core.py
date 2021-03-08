class MobCore:
    def __init__(
        self,
        unique_id: int,
        name: str,
        base_xp: int,
    ):
        self.unique_id = unique_id
        self.name = name
        self.base_xp = base_xp

    def __repr__(self):
        response = "Unique ID: %s" % self.unique_id
        response += "\nName: %s" % self.name
        response += "\nBase XP: %s" % self.base_xp
        return response
