from typing import List

import discord

from commands.command import Command
from tasks.task_helper import stop_task


class Collect(Command):
    def get_description(self):
        return 'Collect your resources.'

    def get_name(self):
        return 'Collect'

    def get_prefixes(self):
        return ['collect', 'c', 'col']

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        await stop_task(msg, player_id)

    def collect_fish(self):
        return
