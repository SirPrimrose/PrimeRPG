#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.idle_embed import IdleEmbed
from primerpg.embeds.shop_embed import ShopEmbed
from primerpg.embeds.task_embed import TaskEmbed
from primerpg.helpers.player_helper import get_player_profile
from primerpg.helpers.task_helper import get_current_player_task


class Shop(Command):
    def get_description(self):
        return "Browse the shop inventory."

    def get_name(self):
        return "Shop"

    def get_prefixes(self):
        return ["shop", "sh", "store"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        profile = get_player_profile(player_id)
        embed = ShopEmbed(msg.author, profile)
        embed_message = await msg.channel.send(embed=embed.generate_embed())
        await embed.connect_reaction_listener(embed_message)
