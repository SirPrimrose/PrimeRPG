from typing import List

from data.entity_base import EntityBase
from persistence.dto.player_core import PlayerCore
from persistence.dto.player_equipment import PlayerEquipment
from persistence.dto.player_inventory_item import PlayerInventoryItem
from persistence.dto.player_skill import PlayerSkill


class PlayerProfile(EntityBase):
    def __init__(
        self,
        core: PlayerCore,
        skills: List[PlayerSkill],
        equipment: List[PlayerEquipment],
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
