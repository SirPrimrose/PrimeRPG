#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class PlayerInventoryItem:
    def __init__(self, player_id: int, item_id: int, quantity: int):
        self.player_id = player_id
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        response = "Player Id: %s" % self.player_id
        response += "\nItem Id: %s" % self.item_id
        response += "\nQuantity: %s" % self.quantity
        return response
