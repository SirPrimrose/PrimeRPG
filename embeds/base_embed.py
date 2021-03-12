import asyncio
from abc import abstractmethod
from typing import List

from discord import Embed, User, Message

from consts import game_client


class BaseEmbed:
    def __init__(self, author: User):
        self.embed_message = None
        self.author = author
        pass

    @abstractmethod
    def generate_embed(self, *args) -> Embed:
        pass

    @abstractmethod
    def get_reaction_emojis(self) -> List[str]:
        pass

    @abstractmethod
    async def handle_fail_to_react(self):
        pass

    @abstractmethod
    async def handle_reaction(self, reaction):
        pass

    async def connect_reaction_listener(self, embed_message: Message) -> None:
        self.embed_message = embed_message
        reaction_list = [
            self.embed_message.add_reaction(emoji)
            for emoji in self.get_reaction_emojis()
        ]
        await self.embed_message.clear_reactions()
        await asyncio.gather(
            *reaction_list,
            self.listen_for_reaction(),
        )

    async def listen_for_reaction(self):
        try:
            reaction, user = await game_client.wait_for(
                "reaction_add",
                timeout=60.0,
                check=self.get_reaction_check(),
            )
        except asyncio.TimeoutError:
            pass
        else:
            await self.handle_reaction(reaction)

    async def update_embed_content(self, relisten_for_reaction=True):
        new_embed = self.generate_embed(True)
        if relisten_for_reaction:
            await asyncio.gather(
                self.embed_message.edit(embed=new_embed), self.listen_for_reaction()
            )
        else:
            await self.embed_message.edit(embed=new_embed)

    def get_reaction_check(self):
        def __reaction_check(reaction, user):
            if user != self.author and user != game_client.user:
                loop = asyncio.get_event_loop()
                loop.create_task(reaction.message.remove_reaction(reaction.emoji, user))
            return (
                user == self.author
                and reaction.message == self.embed_message
                and str(reaction.emoji) in self.get_reaction_emojis()
            )

        return __reaction_check
