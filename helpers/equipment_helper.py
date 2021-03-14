from data.entity_equipment import EntityEquipment
from data.item_amount import ItemAmount
from data.player_profile import PlayerProfile
from helpers.item_helper import give_player_item
from persistence.dto.player_equipment import PlayerEquipment
from persistence.items_persistence import get_item


def unequip_player_item(player_profile: PlayerProfile, equipment: EntityEquipment):
    player_profile.equipment.remove(equipment)
    give_player_item(player_profile, ItemAmount(equipment.item_id, 1))


def equip_player_item(player_profile: PlayerProfile, item_id: int) -> [None, str]:
    item = get_item(item_id)
    cat_id = item.equipment_category_id

    # Check if unequippable
    if item.equipment_category_id == 0:
        return "Item is not equippable"

    # Check if player has enough of item
    inv_item = player_profile.get_inventory_item(item_id)
    if inv_item.quantity < 1:
        return "Not enough of item"

    # Check if player already has item equipped in slot
    equipment = player_profile.get_equipment(cat_id)
    if equipment:
        unequip_player_item(player_profile, equipment)

    give_player_item(player_profile, ItemAmount(item_id, -1))
    player_profile.equipment.append(
        PlayerEquipment(player_profile.core.unique_id, cat_id, item_id)
    )
