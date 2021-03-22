#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List

from discord import User, Embed

from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_world_status_footer
from primerpg.embeds.task_started_embed import TaskStartedEmbed
from primerpg.emojis import (
    task_emojis,
    emoji_from_id,
)
from primerpg.helpers.task_helper import handle_start_task
from primerpg.persistence.dto.task_category import TaskCategory
from primerpg.urls import tasks_url
from primerpg.util import get_key_for_value

_progress_bar_length = 15


class IdleEmbed(BaseEmbed):
    def __init__(self, author: User, categories: list[TaskCategory]):
        super().__init__(author)
        self.categories = categories

    def generate_embed(self, *args) -> Embed:
        embed = Embed(title="Current Status - Idling")
        embed.set_thumbnail(url=tasks_url)

        # Player is idle, show possible tasks
        action_text = ""
        for task_cat in self.categories:
            emoji = emoji_from_id(task_emojis[task_cat.unique_id])
            task_name = task_cat.name
            action_text += "\n{} {}".format(emoji, task_name)
        embed.add_field(name="**Actions**", value=action_text, inline=False)

        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        emojis = []
        for task_cat in self.categories:
            emojis.append(task_emojis[task_cat.unique_id])
        return emojis

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        try:
            task_id = get_key_for_value(task_emojis, reaction_id)
            new_task = handle_start_task(self.author.id, task_id)
            embed = TaskStartedEmbed(self.author, new_task)
            generated_embed = embed.generate_embed()
            await self.embed_message.edit(embed=generated_embed)
        except KeyError:
            await self.embed_message.channel.send("Failed to handle reaction")
