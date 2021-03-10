from discord import User, Embed

import emojis
from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_detailed_stat_field
from text_consts import large_space, small_space
from urls import profile_url

skills_per_line = 3


class ProfileEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__()
        self.player_profile = player_profile
        self.author = author

    def generate_embed(self) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Profile".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=profile_url)
        add_detailed_stat_field(embed, "Stats", self.player_profile)
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
                value += "{2}{0}{3}{1}{2}|".format(
                    skill_emoji, skill_text, large_space, small_space
                )
                skills_on_line += 1

        embed.add_field(name="Skills", value=value, inline=False)
        return embed
