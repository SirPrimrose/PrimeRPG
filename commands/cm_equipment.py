from typing import List

import discord

from commands.command import Command
from embeds.equipment_embed import EquipmentEmbed
from helpers.player_helper import get_player_profile


class Equipment(Command):
    def get_description(self):
        return "Shows your player's equipment in greater detail."

    def get_name(self):
        return "Equipment"

    def get_prefixes(self):
        return ["equipment"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        embed = EquipmentEmbed(player_profile, msg.author)
        await msg.channel.send(embed=embed.generate_embed())
