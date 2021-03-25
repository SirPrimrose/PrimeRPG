#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List


class ItemMoveset:
    def __init__(self, item_id: int, moveset_ids: List[int]):
        self.item_id = item_id
        self.moveset_ids = moveset_ids

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
