from abc import abstractmethod
import discord
from typing import List

class Command:
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
