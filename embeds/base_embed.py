from abc import abstractmethod

from discord import Embed, User, Message


class BaseEmbed:
    def __init__(self, author: User):
        self.embed_message = None
        self.author = author
        pass

    @abstractmethod
    def generate_embed(self) -> Embed:
        pass

    @abstractmethod
    async def connect_reaction_listener(self, embed_message: Message) -> None:
        pass
