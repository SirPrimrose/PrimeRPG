import datetime
from typing import List

import discord

import util
from commands.command import Command


class Weather(Command):
    def get_description(self):
        return 'Check the weather.'

    def get_name(self):
        return 'Weather'

    def get_prefixes(self):
        return ['weather']

    async def run_command(self, msg: discord.Message, args: List[str]):
        response = util.get_in_game_weather(int(datetime.datetime.utcnow().timestamp()))
        return await msg.channel.send(response)
