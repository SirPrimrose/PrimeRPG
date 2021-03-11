from math import floor

from discord import User, Embed, Message

from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed
from embeds.common_embed import pretty_format_skill_level
from emojis import skill_emojis
from text_consts import light_bar, full_bar, no_space
from urls import skills_url
from util import get_skill_category_short_name

progress_bar_length = 20


class SkillsEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__(author)
        self.player_profile = player_profile

    def generate_embed(self) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Skills".format(self.author.name), icon_url=self.author.avatar_url
        )
        embed.set_thumbnail(url=skills_url)
        value = ""
        for skill_emoji, skill_id in skill_emojis.items():
            skill = next(
                filter(lambda s: s.skill_id == skill_id, self.player_profile.skills),
                None,
            )
            progress = skill.calculate_progress_to_next_level()
            full_bars = floor(progress_bar_length * progress)
            light_bars = progress_bar_length - full_bars
            progress_text = full_bars * full_bar + light_bars * light_bar
            value += "{} `{}`{}`{}`\n".format(
                skill_emoji,
                pretty_format_skill_level(skill.level),
                progress_text,
                get_skill_category_short_name(skill_id),
            )
        embed.add_field(
            name=no_space,
            value=value,
            inline=False,
        )
        return embed

    async def connect_reaction_listener(self, embed_message: Message) -> None:
        pass
