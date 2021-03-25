#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.profile_embed import ProfileEmbed
from primerpg.embeds.rank_embed import RankEmbed
from primerpg.helpers.player_helper import get_player_profile


class Rank(Command):
    def get_description(self):
        return "Show your player ranks."

    def get_name(self):
        return "Rank"

    def get_prefixes(self):
        return ["rank", "ranks"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        embed = RankEmbed(player_id, msg.author)
        await msg.channel.send(embed=embed.generate_embed())
