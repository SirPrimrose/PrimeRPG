#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.skills_embed import SkillsEmbed
from primerpg.helpers.player_helper import get_player_profile


class Skills(Command):
    def get_description(self):
        return "Shows your player's skills in greater detail."

    def get_name(self):
        return "Skills"

    def get_prefixes(self):
        return ["skills", "sk", "skill"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        embed = SkillsEmbed(player_profile, msg.author)
        await msg.channel.send(embed=embed.generate_embed())
