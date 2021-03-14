from typing import List

from data.entity_base import EntityBase
from persistence.dto.player_core import PlayerCore
from persistence.dto.player_equipment import PlayerEquipment
from persistence.dto.player_skill import PlayerSkill


class PlayerProfile(EntityBase):
    def __init__(
        self,
        core: PlayerCore,
        skills: List[PlayerSkill],
        equipment: List[PlayerEquipment],
    ):
        super().__init__(core.name, core.avatar_url, skills, equipment)
        self.core = core

    def __repr__(self):
        response = super.__repr__(self)
        response += "\nCore: \n%s" % self.core
        return response

    def get_current_hp(self) -> float:
        return self.core.current_hp

    def set_current_hp(self, new_hp: float) -> None:
        self.core.current_hp = new_hp
