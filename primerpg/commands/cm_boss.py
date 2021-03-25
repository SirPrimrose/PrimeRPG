#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.boss_embed import BossEmbed
from primerpg.helpers.boss_helper import get_boss_profile
from primerpg.helpers.command_usage_helper import set_command_last_usage
from primerpg.helpers.player_helper import get_player_profile
from primerpg.helpers.state_helper import set_player_state, bossfight_state_id


class Boss(Command):
    def get_description(self):
        return "Fight a boss enemy"

    def get_name(self):
        return "Boss"

    def get_prefixes(self):
        return ["boss"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)

        boss_profile = get_boss_profile(player_profile.core.zone_id)

        if boss_profile:
            set_player_state(player_id, bossfight_state_id)
            set_command_last_usage(msg.author.id, self.get_name())
            embed = BossEmbed(msg.author, player_profile, boss_profile)
            embed_message = await msg.channel.send(embed=embed.generate_embed())
            await embed.connect_reaction_listener(embed_message)
        else:
            await msg.channel.send("There are no more bosses to defeat.")
