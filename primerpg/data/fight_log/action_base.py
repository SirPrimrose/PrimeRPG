#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from abc import abstractmethod


class ActionBase:
    def __init__(self, newline: bool = True):
        self.newline = newline

    @abstractmethod
    def get_message(self) -> str:
        pass
