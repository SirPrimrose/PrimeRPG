from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.consts import command_prefix
from primerpg.persistence.player_persistence import get_player


class Data(Command):
    def get_description(self):
        return "Get a player's data."

    def get_name(self):
        return "Data"

    def get_prefixes(self):
        return ["data"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_data = get_player(player_id)
        if player_data is None:
            await msg.channel.send("Create an account with %sstart" % command_prefix)
        else:
            await msg.channel.send(repr(player_data))
