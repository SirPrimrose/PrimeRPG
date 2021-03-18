#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.data.entity_skill import EntitySkill


class MonsterSkill(EntitySkill):
    def __init__(self, mob_id: int, skill_id: int, total_xp: int):
        super().__init__(mob_id, skill_id, total_xp)
