from abc import abstractmethod

from discord import Embed, User, Message


class BaseEmbed:
    def __init__(self):
        pass

    @abstractmethod
    def generate_embed(self) -> Embed:
        pass

    @abstractmethod
    async def connect_reaction_listener(
        self, embed_message: Message, author: User
    ) -> None:
        pass
