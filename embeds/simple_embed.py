from typing import List

from discord import User, Embed

from embeds.base_embed import BaseEmbed


class SimpleEmbed(BaseEmbed):
    def __init__(self, author: User, title: str, content: str):
        super().__init__(author)
        self.title = title
        self.content = content

    def generate_embed(self) -> Embed:
        embed = Embed(title=self.title, description=self.content)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass
