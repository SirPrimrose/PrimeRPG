#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import asyncio
from abc import abstractmethod
from typing import List

from discord import Embed, User, Message

from primerpg.consts import game_client
from primerpg.emojis import extract_id_from_emoji, emoji_from_id


class BaseEmbed:
    def __init__(self, author: User):
        self.embed_message = None
        self.author = author
        pass

    @abstractmethod
    def generate_embed(self, *args) -> Embed:
        pass

    @abstractmethod
    def get_reaction_emojis(self) -> List[int]:
        pass

    @abstractmethod
    async def handle_fail_to_react(self):
        pass

    @abstractmethod
    async def handle_reaction(self, reaction_id: int):
        pass

    # TODO Have this spawn a coroutine for listening for the reaction, so that this function can return
    async def connect_reaction_listener(self, embed_message: Message) -> None:
        self.embed_message = embed_message
        await self.embed_message.clear_reactions()
        await asyncio.gather(
            self._generate_reactions(),
            self.listen_for_reaction(),
        )

    async def _generate_reactions(self):
        reaction_list = [self.embed_message.add_reaction(emoji_from_id(emoji)) for emoji in self.get_reaction_emojis()]
        await asyncio.gather(
            *reaction_list,
        )

    async def listen_for_reaction(self):
        try:
            reaction, user = await game_client.wait_for(
                "reaction_add",
                timeout=60.0,
                check=self.get_reaction_check(),
            )
        except asyncio.TimeoutError:
            await self.handle_fail_to_react()
        else:
            await self.handle_reaction(extract_id_from_emoji(str(reaction)))

    async def update_embed_content(self, relisten_for_reaction=True, regenerate_reactions=False):
        new_embed = self.generate_embed(True)
        actions = [asyncio.create_task(self.embed_message.edit(embed=new_embed))]
        if relisten_for_reaction:
            actions.append(asyncio.create_task(self.listen_for_reaction()))
        if regenerate_reactions:
            await self.embed_message.clear_reactions()
            actions.append(asyncio.create_task(self._generate_reactions()))
        await asyncio.gather(*actions)

    def get_reaction_check(self):
        def __reaction_check(reaction, user):
            if reaction.message == self.embed_message:
                if extract_id_from_emoji(str(reaction.emoji)) not in self.get_reaction_emojis() or (
                    user != self.author and user != game_client.user
                ):
                    loop = asyncio.get_event_loop()
                    loop.create_task(reaction.message.remove_reaction(reaction.emoji, user))
            return (
                user == self.author
                and reaction.message == self.embed_message
                and extract_id_from_emoji(str(reaction.emoji)) in self.get_reaction_emojis()
            )

        return __reaction_check
