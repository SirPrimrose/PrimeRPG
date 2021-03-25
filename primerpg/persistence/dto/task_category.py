#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class TaskCategory:
    def __init__(self, unique_id: int, zone_id: int, name: str):
        self.unique_id = unique_id
        self.zone_id = zone_id
        self.name = name

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
