from discord import User, Embed

import emojis
from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed

skills_per_line = 3


class ProfileEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__()
        self.player_profile = player_profile
        self.author = author

    def generate_embed(self) -> Embed:
        embed = Embed(title="Cool Guy")
        embed.set_author(
            name="{}'s Profile".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(
            url="https://image.flaticon.com/icons/png/128/3075/3075884.png"
        )
        stats_value = "Combat Level: {}\nHP: {}/{}".format(
            self.player_profile.get_combat_level(),
            self.player_profile.current_hp,
            self.player_profile.get_max_hp(),
        )
        embed.add_field(
            name="Stats",
            value=stats_value,
            inline=False,
        )
        value = "\n|"
        skills_on_line = 0
        for skill_emoji, skill_id in emojis.skill_emojis.items():
            if skills_on_line >= skills_per_line:
                skills_on_line = 0
                value += "\n|"
            skill = next(
                filter(lambda s: s.skill_id == skill_id, self.player_profile.skills),
                None,
            )
            if skill:
                skill_level_text = "{}".format(skill.level)
                skill_text = "`{}{}`".format(
                    (2 - len(skill_level_text)) * " ", skill_level_text
                )
                value += "\u2001{}\u2000{}\u2001|".format(skill_emoji, skill_text)
                skills_on_line += 1

        embed.add_field(name="Skills", value=value, inline=False)
        """for skill_emoji, skill_id in emojis.skill_emojis.items():
            skill = next(
                filter(lambda s: s.skill_id == skill_id, self.player_profile.skills),
                None,
            )
            if skill:
                embed.add_field(
                    name=skill_emoji, value=skill.calculate_level(), inline=True
                )"""
        return embed
