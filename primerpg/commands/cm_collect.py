#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.world_embed import WorldEmbed


class World(Command):
    def get_description(self):
        return "Check the time, weather, and fortune."

    def get_name(self):
        return "World"

    def get_prefixes(self):
        return ["world", "weather", "time", "fortune"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        embed = WorldEmbed(msg.author)
        await msg.channel.send(embed=embed.generate_embed())
