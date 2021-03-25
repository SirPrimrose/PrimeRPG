#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class WeightedValue:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
