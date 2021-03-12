from typing import List

import discord

from commands.command import Command
from embeds.recon_embed import ReconEmbed
from helpers.player_helper import get_player_profile, get_mob_profile


class Recon(Command):
    def get_description(self):
        return "Recons to find a random enemy."

    def get_name(self):
        return "Recon"

    def get_prefixes(self):
        return ["recon", "r", "fight"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        mob_profile = get_mob_profile(1)
        embed = ReconEmbed(player_profile, mob_profile, msg.author)
        embed_message = await msg.channel.send(embed=embed.generate_embed())
        await embed.connect_reaction_listener(embed_message)
