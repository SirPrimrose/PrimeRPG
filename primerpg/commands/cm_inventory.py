#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.inventory_embed import InventoryEmbed
from primerpg.helpers.player_helper import get_player_profile


class Inventory(Command):
    def get_description(self):
        return "Show inventory for player."

    def get_name(self):
        return "Inventory"

    def get_prefixes(self):
        return ["inventory", "i"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        profile = get_player_profile(player_id)
        embed = InventoryEmbed(msg.author, profile).generate_embed()
        await msg.channel.send(embed=embed)
