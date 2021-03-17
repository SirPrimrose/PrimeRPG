from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.helpers.player_helper import get_player_profile
from primerpg.helpers.task_helper import handle_collect
from primerpg.persistence.player_task_persistence import get_player_task
from primerpg.util import time_since


class Collect(Command):
    def get_description(self):
        return "Collect your resources."

    def get_name(self):
        return "Collect"

    def get_prefixes(self):
        return ["collect", "c", "col"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        task_core = get_player_task(player_id)
        profile = get_player_profile(player_id)
        task_data = handle_collect(profile, task_core)

        # TODO Move this response to a Task Rewards embed
        response = "Finished {} task. You spent {:.2f} secs collecting.".format(
            task_core.task_id, time_since(task_data.time_started).total_seconds()
        )
        if len(task_data.get_task_rewards()) > 0:
            response += "\n\nYou earned {}".format(task_data.get_task_rewards())
        await msg.channel.send(response)
