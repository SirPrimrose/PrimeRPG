from typing import List

from discord import User, Embed

from embeds.base_embed import BaseEmbed
from persistence.items_persistence import get_item
from urls import backpack_url


class InventoryEmbed(BaseEmbed):
    def __init__(self, items, author: User):
        super().__init__(author)
        self.items = items

    def generate_embed(self) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Inventory".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=backpack_url)
        value = ""
        for item in self.items:
            i = get_item(item.item_id)
            value += "{}: {}\n".format(i.name, item.quantity)
        embed.add_field(
            name="Items",
            value=value if value else "Nothing",
            inline=False,
        )
        return embed

    def get_reaction_emojis(self) -> List[str]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction):
        pass
