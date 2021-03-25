#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class Fish:
    def __init__(
        self,
        unique_id: int,
        item_id: int,
        name: str,
        start_time: str,
        end_time: str,
        weather: str,
        weight: int,
    ):
        self.unique_id = unique_id
        self.item_id = item_id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.weather = weather
        self.weight = weight

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
