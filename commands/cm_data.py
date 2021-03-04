from typing import List

import discord

from persistence.player_persistence import get_player_data
from commands.command import Command
from consts import command_prefix


class Data(Command):
    def get_description(self):
        return "Get a player's data."

    def get_name(self):
        return "Data"

    def get_prefixes(self):
        return ["data"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_data = get_player_data(player_id)
        if player_data is None:
            await msg.channel.send("Create an account with %sstart" % command_prefix)
        else:
            await msg.channel.send(repr(player_data))
