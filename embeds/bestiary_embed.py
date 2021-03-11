from discord import Embed, Message, User

from embeds.base_embed import BaseEmbed


class BestiaryEmbed(BaseEmbed):
    async def connect_reaction_listener(self, embed_message: Message) -> None:
        pass

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
