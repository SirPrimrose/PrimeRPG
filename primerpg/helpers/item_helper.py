#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from math import floor

from primerpg.consts import coin_item_id
from primerpg.data.item_amount import ItemAmount
from primerpg.data.player_profile import PlayerProfile
from primerpg.data.shop_transaction import ShopTransaction
from primerpg.persistence.dto.item import Item
from primerpg.persistence.dto.player_inventory_item import PlayerInventoryItem
from primerpg.persistence.items_persistence import get_item

_sellback_ratio = 0.4


def give_player_item(player_profile: PlayerProfile, item: ItemAmount) -> None:
    current_item = player_profile.get_inventory_item(item.item_id)
    if current_item:
        current_item.quantity += item.quantity
    else:
        current_item = PlayerInventoryItem(player_profile.core.unique_id, item.item_id, item.quantity)
        player_profile.add_inventory_item(current_item)


def attempt_purchase_item(player_profile: PlayerProfile, item: Item, quantity: int) -> ShopTransaction:
    if quantity < 1:
        return ShopTransaction("Must purchase at least 1 of item.", item, quantity, 0)
    coins = player_profile.get_coins()
    total_cost = item.value * quantity
    if coins < total_cost:
        return ShopTransaction("Not enough coins.", item, quantity, total_cost)
    else:
        give_player_item(player_profile, ItemAmount(item.unique_id, quantity))
        give_player_item(player_profile, ItemAmount(coin_item_id, -total_cost))
        return ShopTransaction("", item, quantity, total_cost)


def attempt_sell_item(player_profile: PlayerProfile, item: Item, quantity: int) -> ShopTransaction:
    if quantity < 1:
        return ShopTransaction("Must sell at least 1 of item.", item, quantity, 0)
    player_items = player_profile.get_inventory_item(item.unique_id)
    total_value = floor(item.value * quantity * _sellback_ratio)
    if player_items.quantity < quantity:
        return ShopTransaction("Not enough items.", item, quantity, total_value)
    else:
        give_player_item(player_profile, ItemAmount(item.unique_id, -quantity))
        give_player_item(player_profile, ItemAmount(coin_item_id, total_value))
        return ShopTransaction("", item, quantity, total_value)


def attempt_use_item(player_profile: PlayerProfile, item_id: int, use_count: int = 1) -> (bool, str):
    # TODO Add support for using multiple items at once with use_count
    inventory_item = player_profile.get_inventory_item(item_id)
    item = get_item(item_id)
    if not item.usage_effects:
        return False, "Cannot use {}".format(item.name)
    if inventory_item.quantity < 1:
        return False, "{} did not have any {}".format(player_profile.name, item.name)
    # TODO Store duration effects into table
    give_player_item(player_profile, ItemAmount(item_id, -1))
    effect_text = ""
    for effect in item.usage_effects:
        if effect["type"] == "Current HP":
            if "amount" in effect:
                player_profile.heal_player_profile(effect["amount"])
                effect_text += "{} used a {} and healed {}\n".format(player_profile.name, item.name, effect["amount"])
            else:
                print("No amount listed in {}".format(effect))
    return True, effect_text
