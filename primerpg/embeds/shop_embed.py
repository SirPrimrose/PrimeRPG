#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import User, Embed

from primerpg.data.player_profile import PlayerProfile
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.emojis import prev_page_emoji_id, next_page_emoji_id
from primerpg.persistence.shop_item_persistence import get_shop_items


class ShopEmbed(BaseEmbed):
    def __init__(self, author: User, profile: PlayerProfile):
        super().__init__(author)
        self.profile = profile
        self.current_page = 1
        self.max_page = 2  # profile.core.zone_id

    def generate_embed(self, *args) -> Embed:
        embed = Embed()
        shop_items = get_shop_items(self.current_page)
        field_name = "Shop Page {}/{}".format(self.current_page, self.max_page)
        shop_text = ""
        for shop_item in shop_items:
            shop_text += "\n{}`{}` | {} {} - {}".format(
                ":crossed_swords:", shop_item.get_name(), shop_item.cost, ":coin:", "Item description..."
            )
        if not shop_text:
            shop_text = "There are no shop items for this zone."
        embed.add_field(name=field_name, value=shop_text, inline=False)
        embed.set_footer(text="You have {} coins.".format(self.profile.get_coins()))
        return embed

    def get_reaction_emojis(self) -> List[int]:
        reactions = []
        if self.current_page > 1:
            reactions.append(prev_page_emoji_id)
        if self.current_page < self.max_page:
            reactions.append(next_page_emoji_id)
        return reactions

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == prev_page_emoji_id:
            self.current_page = self.current_page - 1
            await self.update_embed_content(regenerate_reactions=True)
        elif reaction_id == next_page_emoji_id:
            self.current_page = self.current_page + 1
            await self.update_embed_content(regenerate_reactions=True)
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
