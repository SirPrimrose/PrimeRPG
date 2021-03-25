#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from abc import abstractmethod
from typing import List

import discord


class Command:
    def __repr__(self):
        var_text = " ".join(["{0}={1!r}".format(var, value) for var, value in vars(self).items()])
        return "<{0.__class__.__name__} {1}>".format(self, var_text)

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    # Always use lowercase characters for prefixes
    @abstractmethod
    def get_prefixes(self):
        pass

    @abstractmethod
    async def run_command(self, msg: discord.Message, args: List[str]):
        pass
