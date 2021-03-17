from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.helpers.player_helper import delete_player_profile


class Scrub(Command):
    def get_description(self):
        return "End your life."

    def get_name(self):
        return "Scrub"

    def get_prefixes(self):
        return ["scrub", "stop"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        delete_player_profile(player_id)
