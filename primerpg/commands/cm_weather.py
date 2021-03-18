#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg import util
from primerpg.commands.command import Command


class Weather(Command):
    def get_description(self):
        return "Check the weather."

    def get_name(self):
        return "Weather"

    def get_prefixes(self):
        return ["weather"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        response = util.get_current_in_game_weather()
        return await msg.channel.send(response)
