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

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
