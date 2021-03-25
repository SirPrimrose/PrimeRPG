#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List


class Moveset:
    def __init__(self, unique_id: int, move_ids: List[int]):
        self.unique_id = unique_id
        self.move_ids = move_ids

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
