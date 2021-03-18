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
        name: str,
        icon_url: str,
        skills: List[EntitySkill],
        equipment: List[EntityEquipment],
        drops: List[MobDrop],
    ):
        super().__init__(name, icon_url, skills, equipment)
        self.core = core
        self.drops = drops
        self._current_hp = self.get_max_hp()

    def __repr__(self):
        response = super.__repr__(self)
        response += "\nCore: \n%s" % self.core
        return response

    def get_current_hp(self) -> float:
        return self._current_hp

    def set_current_hp(self, new_hp: float) -> None:
        self._current_hp = new_hp