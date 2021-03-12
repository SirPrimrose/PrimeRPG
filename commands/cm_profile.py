from typing import List

import discord

from commands.command import Command
from embeds.profile_embed import ProfileEmbed
from helpers.player_helper import get_player_profile


class Profile(Command):
    def get_description(self):
        return "Show your profile."

    def get_name(self):
        return "Profile"

    def get_prefixes(self):
        return ["profile", "p"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        embed = ProfileEmbed(player_profile, msg.author)
        embed_message = await msg.channel.send(embed=embed.generate_embed())
        await embed.connect_reaction_listener(embed_message)
