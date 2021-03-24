#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List

from primerpg.data.entity_equipment import EntityEquipment
from primerpg.data.entity_skill import EntitySkill
from primerpg.data.mob_profile import MobProfile
from primerpg.persistence.dto.boss_core import BossCore
from primerpg.persistence.dto.mob_drop import MobDrop
from primerpg.persistence.mob_persistence import get_mob


class BossProfile(MobProfile):
    def __init__(
        self,
        core: BossCore,
        skills: List[EntitySkill],
        equipment: List[EntityEquipment],
        drops: List[MobDrop],
    ):
        mob_core = get_mob(core.mob_id)
        super().__init__(mob_core, skills, equipment, drops)
        self.type_strength_ids = core.type_strength_ids
        self.type_weakness_ids = core.type_weakness_ids
