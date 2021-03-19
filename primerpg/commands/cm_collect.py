#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.idle_embed import IdleEmbed
from primerpg.embeds.task_embed import TaskEmbed
from primerpg.embeds.task_stopped_embed import TaskStoppedEmbed
from primerpg.helpers.player_helper import get_player_profile
from primerpg.helpers.task_helper import get_current_player_task, handle_collect_task


class Collect(Command):
    def get_description(self):
        return "Instantly collects an existing task."

    def get_name(self):
        return "Collect"

    def get_prefixes(self):
        return ["collect"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        task = get_current_player_task(player_id)
        if task:
            profile = get_player_profile(player_id)
            new_task = handle_collect_task(profile)
            embed = TaskStoppedEmbed(msg.author, new_task)
            await msg.channel.send(embed=embed.generate_embed())
        else:
            await msg.channel.send("No existing task.")
