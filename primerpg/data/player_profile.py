#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from primerpg.data.entity_base import EntityBase
from primerpg.data.entity_equipment import EntityEquipment
from primerpg.data.entity_skill import EntitySkill
from primerpg.persistence.dto.player_core import PlayerCore
from primerpg.persistence.dto.player_inventory_item import PlayerInventoryItem


class PlayerProfile(EntityBase):
    def __init__(
        self,
        core: PlayerCore,
        skills: List[EntitySkill],
        equipment: List[EntityEquipment],
        inventory: List[PlayerInventoryItem],
    ):
        super().__init__(core.name, core.avatar_url, skills, equipment)
        self.core = core
        self._inventory = inventory
        # Reassign fields to correct typing errors
        self.skills = skills
        self.equipment = equipment

    def __repr__(self):
        response = super.__repr__(self)
        response += "\nCore: \n%s" % self.core
        return response

    def get_current_hp(self) -> float:
        return self.core.current_hp

    def set_current_hp(self, new_hp: float) -> None:
        self.core.current_hp = new_hp

    def get_inventory(self):
        return self._inventory

    def get_inventory_item(self, item_id: int) -> PlayerInventoryItem:
        try:
            result = next(
                filter(
                    lambda item: item.item_id == item_id,
                    self._inventory,
                )
            )
        except StopIteration:
            result = None
        return result

    def add_inventory_item(self, item: PlayerInventoryItem) -> None:
        self._inventory.append(item)
