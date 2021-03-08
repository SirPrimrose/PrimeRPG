from discord import User, Embed

from embeds.base_embed import BaseEmbed
from persistence.inventory_persistence import get_all_inventory_items
from persistence.items_persistence import get_item
from urls import backpack_url


class InventoryEmbed(BaseEmbed):
    def __init__(self, player_id: int, author: User):
        super().__init__()
        self.player_id = player_id
        self.author = author

    def generate_embed(self) -> Embed:
        embed = Embed(title="My Player Inventory")
        embed.set_author(name="My Inventory", icon_url=self.author.avatar_url)
        embed.set_thumbnail(url=backpack_url)
        items = get_all_inventory_items(self.player_id)
        value = ""
        for item in items:
            i = get_item(item.item_id)
            value += "{}: {}\n".format(i.name, item.quantity)
        embed.add_field(
            name="Items",
            value=value,
            inline=False,
        )
        return embed
