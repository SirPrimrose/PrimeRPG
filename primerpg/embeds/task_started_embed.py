#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List

from discord import User, Embed

from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_world_status_footer
from primerpg.tasks.task_base import TaskBase
from primerpg.text_consts import no_space
from primerpg.util import get_current_in_game_time


class TaskStartedEmbed(BaseEmbed):
    def __init__(self, author: User, task: TaskBase):
        super().__init__(author)
        self.task = task

    def generate_embed(self, *args) -> Embed:
        embed = Embed()
        text = "{} started {} at `{}`. Use .task again to check the status.".format(
            self.author.name, self.task.task_name, get_current_in_game_time()
        )
        embed.add_field(name=text, value=no_space)

        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass
