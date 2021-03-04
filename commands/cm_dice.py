import random
import sys
from typing import List

import discord

from commands.command import Command


class Dice(Command):
    def get_description(self):
        return 'Roll a dice.'

    def get_name(self):
        return 'Dice'

    def get_prefixes(self):
        return ['dice', 'roll']

    async def run_command(self, msg: discord.Message, args: List[str]):
        try:
            min = 1
            max = 100
            if len(args) == 1:
                max = int(args[0])
            if len(args) >= 2:
                min = int(args[0])
                max = int(args[1])
            num = random.randrange(min, max)
            await msg.channel.send('You rolled a {0}'.format(num))
        except ValueError:
            print("Unexpected error:", sys.exc_info()[1])
            await msg.channel.send('Please enter a range of two valid numbers, or a single number greater than 1.')