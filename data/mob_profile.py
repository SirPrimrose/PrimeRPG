from typing import List

from data.entity_base import EntityBase
from data.entity_equipment import EntityEquipment
from data.entity_skill import EntitySkill
from persistence.dto.mob_core import MobCore
from persistence.dto.mob_drop import MobDrop
from persistence.dto.mob_equipment import MobEquipment
from persistence.dto.mob_skill import MobSkill


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
