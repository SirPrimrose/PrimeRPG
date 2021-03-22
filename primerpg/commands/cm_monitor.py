#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: iKosm

from typing import List

import discord
import monitor

from primerpg.commands.command import Command


class Monitor(Command):
    def get_description(self):
        return "Displays server information"

    def get_name(self):
        return "Monitor"

    def get_prefixes(self):
        return ["monitor", "mon"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        await msg.channel.send(monitor.ram_monitor(True))
