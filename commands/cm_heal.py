from typing import List

import discord

from commands.command import Command
from helpers.player_helper import get_player_profile, save_player_profile


class Heal(Command):
    def get_description(self):
        return "Heal a player."

    def get_name(self):
        return "Heal"

    def get_prefixes(self):
        return ["heal"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        player_profile.current_hp = player_profile.get_max_hp()
        save_player_profile(player_profile)
        await msg.channel.send("Healed {}".format(msg.author.name))
