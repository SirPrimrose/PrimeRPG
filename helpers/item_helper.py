from data.player_inventory_item import PlayerInventoryItem
from persistence.inventory_persistence import (
    update_inventory_item,
    insert_inventory_item,
    get_inventory_item,
)


def give_player_item(player_id, item_id, amount):
    current_item = get_inventory_item(player_id, item_id)
    if current_item:
        current_item.quantity += amount
        update_inventory_item(current_item)
    else:
        current_item = PlayerInventoryItem(player_id, item_id, amount)
        insert_inventory_item(current_item)
