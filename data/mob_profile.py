from typing import List

from data.entity_base import EntityBase
from data.entity_equipment import EntityEquipment
from data.entity_skill import EntitySkill
from data.mob_core import MobCore


class MobProfile(EntityBase):
    def __init__(
        self,
        core: MobCore,
        name: str,
        icon_url: str,
        skills: List[EntitySkill],
        equipment: List[EntityEquipment],
    ):
        super().__init__(name, icon_url, skills, equipment)
        self.core = core
        self.current_hp = self.get_max_hp()

    def __repr__(self):
        response = super.__repr__(self)
        response += "\nCore: \n%s" % self.core
        return response
