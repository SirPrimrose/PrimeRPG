#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import User, Embed

from primerpg.data.shop_transaction import ShopTransaction
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.emojis import auto_equip_emoji_id
from primerpg.helpers.equipment_helper import equip_player_item
from primerpg.helpers.player_helper import get_player_profile, save_player_profile


class PurchaseResultEmbed(BaseEmbed):
    def __init__(self, author: User, transaction: ShopTransaction):
        super().__init__(author)
        self.transaction = transaction

    def generate_embed(self, *args) -> Embed:
        if self.transaction.err_message:
            title = "Failed to purchase {}".format(self.transaction.item.name)
            content = self.transaction.err_message
        else:
            title = "Purchase success"
            content = "{0} bought {1.quantity} {1.item.name} for {1.total_cost} coins".format(
                self.author.name, self.transaction
            )
        embed = Embed(title=title, description=content)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        if self.transaction.item.equipment_category_id != 0:
            return [auto_equip_emoji_id]
        else:
            return []

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == auto_equip_emoji_id:
            player_profile = get_player_profile(self.author.id)
            response = equip_player_item(player_profile, self.transaction.item.unique_id)
            save_player_profile(player_profile)
            await self.embed_message.channel.send("Equip success." if not response else response)
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
