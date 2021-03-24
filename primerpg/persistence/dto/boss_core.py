#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class BossCore:
    def __init__(self, mob_id: int, zone_id: int, type_strengths: list[int], type_weaknesses: list[int]):
        self.mob_id = mob_id
        self.zone_id = zone_id
        self.type_strength_ids = type_strengths
        self.type_weakness_ids = type_weaknesses

    def __repr__(self):
        response = "mob_id: %s" % self.mob_id
        response += "\nzone_id: %s" % self.zone_id
        response += "\ntype_strengths: %s" % self.type_strength_ids
        response += "\ntype_weaknesses: %s" % self.type_weakness_ids
        return response
