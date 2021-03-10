from typing import List

import discord

from commands.command import Command
from embeds.recon_embed import ReconEmbed
from helpers.battle_helper import sim_fight
from helpers.player_helper import get_player_profile


class Recon(Command):
    def get_description(self):
        return "Recons to find a random enemy."

    def get_name(self):
        return "Recon"

    def get_prefixes(self):
        return ["recon", "r"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        dupe_profile = get_player_profile(player_id)
        sim_fight(player_profile, dupe_profile)
        embed = ReconEmbed(player_profile, dupe_profile).generate_embed()
        await msg.channel.send(embed=embed)
