from typing import List

import discord

from commands.command import Command
from consts import fishing_task
from persistence.player_persistence import get_player_data, update_player_data
from persistence.task_helper import start_task
from player import idle_state, gathering_state


class Fish(Command):
    def get_description(self):
        return 'Fish some fish.'

    def get_name(self):
        return 'Fish'

    def get_prefixes(self):
        return ['fish', 'fishing', 'fsh']

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        await start_task(msg, player_id, fishing_task)
