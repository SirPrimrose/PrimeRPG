class Move:
    def __init__(
        self,
        unique_id: int,
        power: int,
        damage_type_id: int,
        scaling_equipment_stat_id: int,
        success_chance: float,
        name: str,
    ):
        self.unique_id = unique_id
        self.power = power
        self.damage_type_id = damage_type_id
        self.scaling_equipment_stat_id = scaling_equipment_stat_id
        self.success_chance = success_chance
        self.name = name
