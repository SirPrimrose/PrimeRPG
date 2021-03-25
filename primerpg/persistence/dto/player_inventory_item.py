#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class PlayerInventoryItem:
    def __init__(self, player_id: int, item_id: int, quantity: int):
        self.player_id = player_id
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
