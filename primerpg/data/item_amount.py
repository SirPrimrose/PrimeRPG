#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class ItemAmount:
    def __init__(self, item_id: int, quantity: int):
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        response = "Item Id: %s" % self.item_id
        response += "\nQuantity: %s" % self.quantity
        return response
