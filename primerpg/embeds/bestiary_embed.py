from typing import List

from discord import Embed, User

from primerpg.embeds.base_embed import BaseEmbed


class BestiaryEmbed(BaseEmbed):
    def __init__(self, author: User):
        super().__init__(author)

    def generate_embed(self) -> Embed:
        embed = Embed(
            title="Slime",
            description="Slimes are bouncy, lop-sided pieces of shit commonly found in swamp biomes and, "
            "occasionally, deep underground.",
        )
        embed.set_author(
            name="Bestiary",
            icon_url="https://freeiconshop.com/wp-content/uploads/edd/book-flat.png",
        )
        embed.set_thumbnail(url="https://i.imgur.com/RskTsQK.png")
        return embed

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass
