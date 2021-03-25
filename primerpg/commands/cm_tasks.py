#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.embeds.idle_embed import IdleEmbed
from primerpg.embeds.task_embed import TaskEmbed
from primerpg.helpers.task_helper import get_current_player_task
from primerpg.persistence.player_persistence import get_player_core
from primerpg.persistence.task_category_persistence import get_task_categories


class Tasks(Command):
    def get_description(self):
        return "See the task status or start a new task."

    def get_name(self):
        return "Tasks"

    def get_prefixes(self):
        return [
            "tasks",
            "task",
            "t",
            "fish",
            "fishing",
            "mine",
            "mining",
            "chop",
            "wood",
            "woodcutting",
            "farming",
            "foraging",
        ]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        task = get_current_player_task(player_id)
        player = get_player_core(player_id)
        if task:
            embed = TaskEmbed(msg.author, task)
        else:
            categories = get_task_categories(player.zone_id)
            embed = IdleEmbed(msg.author, categories)
        embed_message = await msg.channel.send(embed=embed.generate_embed())
        await embed.connect_reaction_listener(embed_message)
