#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.data.entity_equipment import EntityEquipment
from primerpg.data.item_amount import ItemAmount
from primerpg.data.player_profile import PlayerProfile
from primerpg.helpers.item_helper import give_player_item
from primerpg.persistence.items_persistence import get_item


def unequip_player_item(player_profile: PlayerProfile, item_id: int):
    item = get_item(item_id)
    cat_id = item.equipment_category_id
    equipment = player_profile.get_equipment(cat_id)
    if equipment:
        player_profile.equipment.remove(equipment)
        give_player_item(player_profile, ItemAmount(equipment.item_id, 1))


# TODO Account for equipment categories that have multiple slots
def equip_player_item(player_profile: PlayerProfile, item_id: int) -> [None, str]:
    item = get_item(item_id)
    cat_id = item.equipment_category_id

    # Check if unequippable
    if item.equipment_category_id == 0:
        return "Item is not equippable"

    # Check if player already has this item equipped in slot
    current_equipment = player_profile.get_equipment(cat_id)
    if current_equipment and current_equipment.item_id == item_id:
        return "Already equipped this item"

    # Check if player has enough of item
    inv_item = player_profile.get_inventory_item(item_id)
    if not inv_item or inv_item.quantity < 1:
        return "Not enough of item"

    # Auto unequip items equipped in this slot
    if current_equipment:
        unequip_player_item(player_profile, item_id)

    give_player_item(player_profile, ItemAmount(item_id, -1))
    player_profile.equipment.append(EntityEquipment(player_profile.core.unique_id, cat_id, item_id))
