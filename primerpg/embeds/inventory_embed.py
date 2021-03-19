#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from collections import OrderedDict
from typing import List, OrderedDict as OrderedDictType

from discord import User, Embed

from primerpg.data_cache import (
    get_item_category_name,
    get_item_name,
    get_item_category_id,
)
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.persistence.dto.player_inventory_item import PlayerInventoryItem
from primerpg.urls import backpack_url


class InventoryEmbed(BaseEmbed):
    def __init__(
        self,
        items: List[PlayerInventoryItem],
        author: User,
    ):
        super().__init__(author)
        self.categorized_items = self._organize_categories(items)

    def generate_embed(self, *args) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Inventory".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=backpack_url)
        for cat_id, cat_item_list in self.categorized_items.items():
            # Skip the "Hidden" category of items
            if cat_id == 0:
                continue
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

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass

    def _organize_categories(self, items: List[PlayerInventoryItem]) -> OrderedDictType[int, List[PlayerInventoryItem]]:
        cat_items = {}
        for item in items:
            cat = get_item_category_id(item.item_id)
            if cat in cat_items:
                cat_items[cat].append(item)
            else:
                cat_items[cat] = [item]
        return OrderedDict(sorted(cat_items.items()))
