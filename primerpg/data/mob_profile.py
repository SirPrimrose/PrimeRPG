#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from primerpg.data.entity_base import EntityBase
from primerpg.data.entity_equipment import EntityEquipment
from primerpg.data.entity_skill import EntitySkill
from primerpg.persistence.dto.mob_core import MobCore
from primerpg.persistence.dto.mob_drop import MobDrop


class MobProfile(EntityBase):
    def __init__(
        self,
        core: MobCore,
        skills: List[EntitySkill],
        equipment: List[EntityEquipment],
        drops: List[MobDrop],
    ):
        super().__init__(core.name, core.icon_url, skills, equipment)
        self.drops = drops
        self._current_hp = self.get_max_hp()
