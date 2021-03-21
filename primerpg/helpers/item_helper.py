#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.consts import coin_item_id
from primerpg.data.item_amount import ItemAmount
from primerpg.data.player_profile import PlayerProfile
from primerpg.data.shop_transaction import ShopTransaction
from primerpg.persistence.dto.player_inventory_item import PlayerInventoryItem
from primerpg.persistence.dto.shop_item import ShopItem


def give_player_item(player_profile: PlayerProfile, item: ItemAmount) -> None:
    current_item = player_profile.get_inventory_item(item.item_id)
    if current_item:
        current_item.quantity += item.quantity
    else:
        current_item = PlayerInventoryItem(player_profile.core.unique_id, item.item_id, item.quantity)
        player_profile.add_inventory_item(current_item)


def attempt_purchase_item(player_profile: PlayerProfile, item: ShopItem, quantity: int) -> ShopTransaction:
    coins = player_profile.get_coins()
    total_cost = item.cost * quantity
    if coins < total_cost:
        return ShopTransaction("Not enough coins.", item.get_name(), quantity, total_cost)
    else:
        give_player_item(player_profile, ItemAmount(item.item_id, quantity))
        give_player_item(player_profile, ItemAmount(coin_item_id, -total_cost))
        return ShopTransaction("", item.get_name(), quantity, total_cost)


def attempt_use_item(player_profile: PlayerProfile, item_id: int):
    current_item = player_profile.get_inventory_item(item_id)
    if current_item.quantity < 1:
        return "Did not have enough items"
    # TODO Allow for xp and item gains (lootboxes?, genie lamps?)
    # TODO Store duration effects into table
    # effects: List[Dict] = get_item_effects(item_id)
    effects = [{"type": "Current HP", "amount": 100}]
    if effects:
        give_player_item(player_profile, ItemAmount(item_id, -1))
        for effect in effects:
            if effect["type"] == "Current HP":
                if "amount" in effect:
                    player_profile.heal_player_profile(effect["amount"])
                    return True
                else:
                    print("No amount listed in {}".format(effect))
    return False
