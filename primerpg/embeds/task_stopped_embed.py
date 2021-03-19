#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List

from discord import User, Embed

from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_world_status_footer
from primerpg.tasks.task_base import TaskBase


class TaskStoppedEmbed(BaseEmbed):
    def __init__(self, author: User, task: TaskBase):
        super().__init__(author)
        self.task = task

    def generate_embed(self, *args) -> Embed:
        embed = Embed(title="Stopped task:", description=str(self.task))

        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass
