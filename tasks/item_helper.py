from data.player_inventory_item import PlayerInventoryItem
from persistence import inventory_persistence


def give_player_item(player_id, item_id, amount):
    current_item = inventory_persistence.get_inventory_data(player_id, item_id)
    if current_item:
        current_item.quantity += amount
        inventory_persistence.update_inventory_data(current_item)
    else:
        current_item = PlayerInventoryItem(player_id, item_id, amount)
        inventory_persistence.insert_inventory_data(current_item)
