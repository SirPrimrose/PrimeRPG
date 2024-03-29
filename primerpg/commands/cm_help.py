#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg import command_handler, consts
from primerpg.commands.command import Command


class Help(Command):
    def get_description(self):
        return "Lists all commands"

    def get_name(self):
        return "Help"

    def get_prefixes(self):
        return ["help", "info", "h", "?"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        response = "Commands:\nAdd %s before any command" % consts.command_prefix
        for command in command_handler.command_registry:
            response += "\n`{0}`".format(command.get_name())
        await msg.channel.send(response)
