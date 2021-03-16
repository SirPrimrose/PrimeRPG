from typing import List

import discord

from commands.command import Command
from consts import fishing_task_id
from helpers.task_helper import handle_start_task


class Fish(Command):
    def get_description(self):
        return "Fish some fish."

    def get_name(self):
        return "Fish"

    def get_prefixes(self):
        return ["fish", "fishing", "fsh"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        handle_start_task(player_id, fishing_task_id)
        await msg.channel.send("Task attempted to start")
