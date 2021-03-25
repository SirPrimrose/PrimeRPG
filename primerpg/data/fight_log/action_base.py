#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from abc import abstractmethod


class ActionBase:
    def __init__(self, newline: bool = True):
        self.newline = newline

    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)

    @abstractmethod
    def get_message(self) -> str:
        pass
