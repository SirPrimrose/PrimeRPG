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
        ig_time = util.get_in_game_time()
        hours, remainder = divmod(ig_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        response = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        return await msg.channel.send(response)
