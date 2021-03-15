from typing import List

import discord

from commands.command import Command
from helpers.player_helper import get_player_profile
from helpers.task_helper import handle_stop_task
from persistence.task_persistence import get_player_task


class Collect(Command):
    def get_description(self):
        return "Collect your resources."

    def get_name(self):
        return "Collect"

    def get_prefixes(self):
        return ["collect", "c", "col"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        task = get_player_task(player_id)
        profile = get_player_profile(player_id)
        rewards, length = handle_stop_task(msg, profile, task)

        if rewards:
            # TODO Move this response to a Task Rewards embed
            response = "Finished {} task. You spent {:.2f} secs collecting.".format(
                task.task, length.total_seconds()
            )
            if len(rewards) > 0:
                response += "\n\nYou earned {}".format(rewards)
            await msg.channel.send(response)

    def collect_fish(self):
        return
