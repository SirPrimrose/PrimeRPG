from abc import abstractmethod

from discord import Embed


class BaseEmbed:
    def __init__(self):
        pass

    @abstractmethod
    def generate_embed(self) -> Embed:
        pass
