#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import sys
from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.data_cache import get_item_id


class Add(Command):
    def get_description(self):
        return "Add some stuff."

    def get_name(self):
        return "Add"

    def get_prefixes(self):
        return ["add", "sum"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        try:
            item_name = args[1]
            item_id = get_item_id(item_name)
            if item_id:
                await msg.channel.send("Item ID:".format(item_id))
            else:
                await msg.channel.send("Item not found.")
        except ValueError:
            await msg.channel.send("Please enter all arguments as numbers.")
