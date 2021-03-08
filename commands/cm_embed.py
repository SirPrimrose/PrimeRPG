from typing import List

import discord

from commands.command import Command
from embeds.profile_embed import ProfileEmbed
from helpers.player_helper import get_player_profile


async def test_profile_embed(msg):
    player_id = msg.author.id
    player_profile = get_player_profile(player_id)
    embed = ProfileEmbed(player_profile, msg.author).generate_embed()
    await msg.channel.send(embed=embed)


class EmbedCommand(Command):
    def get_description(self):
        return "Get a test embed."

    def get_name(self):
        return "Embed"

    def get_prefixes(self):
        return ["embed"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        await test_profile_embed(msg)
