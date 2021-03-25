#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class MobDrop:
    def __init__(self, mob_id: int, item_id: int, drop_rate: float, mean: float, std_dev: float):
        self.mob_id = mob_id
        self.item_id = item_id
        self.drop_rate = drop_rate
        self.mean = mean
        self.std_dev = std_dev

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
