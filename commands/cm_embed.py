from typing import List

import discord

from commands.command import Command
from embeds.bestiary_embed import BestiaryEmbed
from embeds.inventory_embed import InventoryEmbed


async def inventory_embed(msg):
    player_id = msg.author.id
    embed = InventoryEmbed(player_id, msg.author).generate_embed()
    await msg.channel.send(embed=embed)


async def bestiary_embed(msg):
    embed = BestiaryEmbed(msg.author).generate_embed()
    await msg.channel.send(embed=embed)


class EmbedCommand(Command):
    def get_description(self):
        return "Get a test embed."

    def get_name(self):
        return "Embed"

    def get_prefixes(self):
        return ["embed"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        await bestiary_embed(msg)
