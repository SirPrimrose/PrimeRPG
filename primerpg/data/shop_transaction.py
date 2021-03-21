#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class ShopTransaction:
    def __init__(self, err_message: str, item_name: str, quantity: int, total_cost: int):
        self.err_message = err_message
        self.item_name = item_name
        self.quantity = quantity
        self.total_cost = total_cost
