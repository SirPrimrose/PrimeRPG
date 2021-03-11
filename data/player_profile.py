from typing import List

from data.entity_base import EntityBase
from data.player_core import PlayerCore
from data.player_equipment import PlayerEquipment
from data.player_skill import PlayerSkill


class PlayerProfile(EntityBase):
    def __init__(
        self,
        core: PlayerCore,
        skills: List[PlayerSkill],
        equipment: List[PlayerEquipment],
    ):
        super().__init__(core.name, core.avatar_url, skills, equipment, core.current_hp)
        self.core = core

    def __repr__(self):
        response = super.__repr__(self)
        response += "\nCore: \n%s" % self.core
        return response
