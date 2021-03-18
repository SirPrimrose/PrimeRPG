#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import sys
from typing import List

import discord

from primerpg.commands.command import Command


class Add(Command):
    def get_description(self):
        return "Add some stuff."

    def get_name(self):
        return "Add"

    def get_prefixes(self):
        return ["add", "sum"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        try:
            total = sum(float(x) for x in args)
            await msg.channel.send("Sum: {0}".format(total))
        except ValueError:
            print("Unexpected error:", sys.exc_info()[1])
            await msg.channel.send("Please enter all arguments as numbers.")
