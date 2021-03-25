#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm


class SkillCategory:
    def __init__(self, unique_id: int, name: str, short_name: str):
        self.unique_id = unique_id
        self.name = name
        self.short_name = short_name

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)
