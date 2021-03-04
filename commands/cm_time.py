from typing import List

import discord

import util
from commands.command import Command


class Time(Command):
    def get_description(self):
        return 'Check the time.'

    def get_name(self):
        return 'Time'

    def get_prefixes(self):
        return ['time', 'clock']

    async def run_command(self, msg: discord.Message, args: List[str]):
        ig_time = util.get_current_in_game_time()
        response = util.time_delta_to_str(ig_time)
        return await msg.channel.send(response)