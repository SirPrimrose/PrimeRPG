from typing import List

import discord

from commands.command import Command
from embeds.inventory_embed import InventoryEmbed
from persistence.inventory_persistence import get_all_inventory_items


class Inventory(Command):
    def get_description(self):
        return "Show inventory for player."

    def get_name(self):
        return "Inventory"

    def get_prefixes(self):
        return ["inventory", "i"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        items = get_all_inventory_items(player_id)
        embed = InventoryEmbed(items, msg.author).generate_embed()
        await msg.channel.send(embed=embed)
