#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.boss_embed import BossEmbed
from primerpg.helpers.mob_helper import get_mob_profile
from primerpg.helpers.player_helper import get_player_profile
from primerpg.helpers.state_helper import set_player_state, bossfight_state_id
from primerpg.persistence.mob_persistence import get_all_mobs
from primerpg.util import get_random_from_weighted_list


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

        mob_list = get_all_mobs()
        random_mob = get_random_from_weighted_list(mob_list)
        mob_profile = get_mob_profile(random_mob.unique_id)

        set_player_state(player_id, bossfight_state_id)
        embed = BossEmbed(msg.author, player_profile, mob_profile)
        embed_message = await msg.channel.send(embed=embed.generate_embed())
        await embed.connect_reaction_listener(embed_message)
