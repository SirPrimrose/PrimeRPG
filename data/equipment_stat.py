class EquipmentStat:
    def __init__(
        self,
        item_id: int,
        skill_category_id: int,
        scaling: int,
        bonus: int,
    ):
        self.item_id = item_id
        self.skill_category_id = skill_category_id
        self.scaling = scaling
        self.bonus = bonus

    def __repr__(self):
        response = "Item Id: %s" % self.item_id
        response += "\nSkill Category Id: %s" % self.skill_category_id
        response += "\nScaling: %s" % self.scaling
        response += "\nBonus: %s" % self.bonus
        return response
