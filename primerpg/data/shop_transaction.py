#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from primerpg.persistence.dto.item import Item


class ShopTransaction:
    def __init__(self, err_message: str, item: Item, quantity: int, total_cost: int):
        self.err_message = err_message
        self.item = item
        self.quantity = quantity
        self.total_cost = total_cost
