#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from primerpg.consts import coin_item_id
from primerpg.data.item_amount import ItemAmount
from primerpg.data.player_profile import PlayerProfile
from primerpg.persistence.dto.player_inventory_item import PlayerInventoryItem
from primerpg.persistence.dto.shop_item import ShopItem


def give_player_item(player_profile: PlayerProfile, item: ItemAmount) -> None:
    current_item = player_profile.get_inventory_item(item.item_id)
    if current_item:
        current_item.quantity += item.quantity
    else:
        current_item = PlayerInventoryItem(player_profile.core.unique_id, item.item_id, item.quantity)
        player_profile.add_inventory_item(current_item)


class ShopTransaction:
    def __init__(self, err_message: str, item_name: str, quantity: int, total_cost: int):
        self.err_message = err_message
        self.item_name = item_name
        self.quantity = quantity
        self.total_cost = total_cost


def attempt_purchase_item(player_profile: PlayerProfile, item: ShopItem, quantity: int) -> ShopTransaction:
    coins = player_profile.get_coins()
    total_cost = item.cost * quantity
    if coins < total_cost:
        return ShopTransaction("Not enough coins.", item.get_name(), quantity, total_cost)
    else:
        give_player_item(player_profile, ItemAmount(item.item_id, quantity))
        give_player_item(player_profile, ItemAmount(coin_item_id, -total_cost))
        return ShopTransaction("Not enough coins.", item.get_name(), quantity, total_cost)
