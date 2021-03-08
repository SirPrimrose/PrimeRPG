from discord import User, Embed

import emojis
from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed


class ProfileEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__()
        self.player_profile = player_profile
        self.author = author

    def generate_embed(self) -> Embed:
        embed = Embed(title="My Player Title")
        embed.set_author(name="My Profile", icon_url=self.author.avatar_url)
        embed.set_thumbnail(url=self.author.avatar_url)
        embed.add_field(
            name="Stats",
            value="Combat Level: 47\nHP: 78/120\nCurrent Zone: Grasslands",
            inline=False,
        )
        embed.add_field(name="\u200b", value="**Skills**", inline=False)
        for skill_emoji, skill_id in emojis.skill_emojis.items():
            skill = next(
                filter(lambda s: s.skill_id == skill_id, self.player_profile.skills),
                None,
            )
            if skill:
                embed.add_field(
                    name=skill_emoji, value=skill.calculate_level(), inline=True
                )
        return embed
