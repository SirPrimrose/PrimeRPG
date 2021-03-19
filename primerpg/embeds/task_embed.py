#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from math import floor
from typing import List, Optional

from discord import User, Embed

from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_world_status_footer
from primerpg.embeds.task_stopped_embed import TaskStoppedEmbed
from primerpg.emojis import (
    letter_f_high_emoji_id,
    collect_emoji_id,
)
from primerpg.helpers.player_helper import get_player_profile
from primerpg.helpers.task_helper import handle_collect_task
from primerpg.tasks.task_base import TaskBase
from primerpg.text_consts import full_bar, light_bar
from primerpg.util import get_in_game_time

_progress_bar_length = 15


class TaskEmbed(BaseEmbed):
    def __init__(self, author: User, task: Optional[TaskBase]):
        super().__init__(author)
        self.task = task

    def generate_embed(self, *args) -> Embed:
        embed = Embed(title="Current Status - {}".format(self.task.task_name))
        # Player has task, show task details
        current_attempts = self.task.get_task_attempt_count()
        attempt_progress = self.task.get_current_attempt_progress()
        full_bars = floor(_progress_bar_length * attempt_progress)
        light_bars = _progress_bar_length - full_bars
        progress_text = full_bars * full_bar + light_bars * light_bar
        embed.add_field(
            name="**Status**",
            value="Started at `{}`\nCollection Attempts:\n`{}`{}`{}` (max at {})".format(
                get_in_game_time(self.task.time_started),
                current_attempts,
                progress_text,
                current_attempts + 1,
                self.task.get_max_task_attempts(),
            ),
            inline=False,
        )
        embed.add_field(name="**Actions**", value="{} Collect".format(":basket:"), inline=False)

        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return [collect_emoji_id]

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == collect_emoji_id:
            profile = get_player_profile(self.author.id)
            new_task = handle_collect_task(profile)
            embed = TaskStoppedEmbed(self.author, new_task)
            generated_embed = embed.generate_embed()
            await self.embed_message.edit(embed=generated_embed)
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
