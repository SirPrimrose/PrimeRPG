from typing import List

import discord

from commands.command import Command
from helpers.battle_helper import sim_fight
from helpers.player_helper import get_player_profile


class Fight(Command):
    def get_description(self):
        return "Fight a random enemy."

    def get_name(self):
        return "Fight"

    def get_prefixes(self):
        return ["fight", "f"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        dupe_profile = get_player_profile(player_id)
        sim_fight(player_profile, dupe_profile)
        # await msg.channel.send(repr(player_profile))