#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.recon_embed import ReconEmbed
from primerpg.helpers.mob_helper import get_mob_profile
from primerpg.helpers.player_helper import get_player_profile
from primerpg.helpers.state_helper import recon_state_id, set_player_state
from primerpg.persistence.mob_persistence import get_all_mobs
from primerpg.util import get_random_from_weighted_list


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

        mob_list = get_all_mobs()
        random_mob = get_random_from_weighted_list(mob_list)
        mob_profile = get_mob_profile(random_mob.unique_id)

        set_player_state(player_id, recon_state_id)
        embed = ReconEmbed(player_profile, mob_profile, msg.author)
        embed_message = await msg.channel.send(embed=embed.generate_embed())
        await embed.connect_reaction_listener(embed_message)
