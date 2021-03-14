from collections import OrderedDict
from typing import List, OrderedDict as OrderedDictType

from discord import User, Embed

from embeds.base_embed import BaseEmbed
from persistence.dto.player_inventory_item import PlayerInventoryItem
from urls import backpack_url
from util import get_item_category, get_item_category_name, get_item_name


class InventoryEmbed(BaseEmbed):
    def __init__(
        self,
        items: List[PlayerInventoryItem],
        author: User,
    ):
        super().__init__(author)
        self.categorized_items = self._organize_categories(items)

    def generate_embed(self) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Inventory".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=backpack_url)
        for cat_id, cat_item_list in self.categorized_items.items():
            cat_text = ""
            for item in cat_item_list:
                item_name = get_item_name(item.item_id)
                if item.quantity > 0:
                    cat_text += "{}: {}\n".format(item_name, item.quantity)
            if cat_text:
                embed.add_field(
                    name=get_item_category_name(cat_id),
                    value=cat_text,
                    inline=True,
                )
        return embed

    def get_reaction_emojis(self) -> List[str]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction):
        pass

    def _organize_categories(
        self, items: List[PlayerInventoryItem]
    ) -> OrderedDictType[int, List[PlayerInventoryItem]]:
        cat_items = {}
        for item in items:
            cat = get_item_category(item.item_id)
            if cat in cat_items:
                cat_items[cat].append(item)
            else:
                cat_items[cat] = [item]
        return OrderedDict(sorted(cat_items.items()))
