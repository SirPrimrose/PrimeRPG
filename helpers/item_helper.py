from data.item_amount import ItemAmount
from data.player_profile import PlayerProfile
from persistence.dto.player_inventory_item import PlayerInventoryItem


def give_player_item(player_profile: PlayerProfile, item: ItemAmount) -> None:
    current_item = player_profile.get_inventory_item(item.item_id)
    if current_item:
        current_item.quantity += item.quantity
    else:
        current_item = PlayerInventoryItem(
            player_profile.core.unique_id, item.item_id, item.quantity
        )
        player_profile.add_inventory_item(current_item)
