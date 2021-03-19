#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import User, Embed

from primerpg.embeds.base_embed import BaseEmbed
from primerpg.util import get_current_in_game_time, get_current_in_game_weather


class WorldEmbed(BaseEmbed):
    def __init__(self, author: User):
        super().__init__(author)

    def generate_embed(self, *args) -> Embed:
        embed = Embed()
        # TODO Add emojis for weather states
        embed.add_field(name="**Time**", value=get_current_in_game_time(), inline=False)
        embed.add_field(name="**Weather**", value=get_current_in_game_weather(), inline=False)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass
