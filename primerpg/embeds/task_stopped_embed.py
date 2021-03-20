#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List

from discord import User, Embed

from primerpg.data_cache import get_item_name
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_world_status_footer
from primerpg.tasks.task_base import TaskBase
from primerpg.urls import tasks_url


class TaskStoppedEmbed(BaseEmbed):
    def __init__(self, author: User, task: TaskBase):
        super().__init__(author)
        self.task = task

    def generate_embed(self, *args) -> Embed:
        embed = Embed(title=self.task.get_results_string(self.author))
        embed.set_thumbnail(url=tasks_url)

        rewards_text = ""
        for reward in self.task.get_task_rewards():
            if reward.quantity > 0:
                item_name = get_item_name(reward.item_id)
                rewards_text += "\n{}: {}".format(item_name, reward.quantity)

        if rewards_text:
            embed.add_field(name="**Results**", value="Minnow: 1", inline=False)

        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass
