#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import User, Embed

from primerpg.data.player_profile import PlayerProfile
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_detailed_stat_field, pretty_format_skill_level, heal_player
from primerpg.emojis import skill_emojis, heal_emoji_id, emoji_from_id
from primerpg.helpers.player_helper import hospital_service
from primerpg.text_consts import large_space, half_space
from primerpg.urls import profile_url

skills_per_line = 3


class ProfileEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__(author)
        self.player_profile = player_profile
        self.author = author

    def generate_embed(self, recently_healed=False, *args) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Profile".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=profile_url)
        add_detailed_stat_field(embed, "Stats", self.player_profile, recently_healed=recently_healed)
        value = "\n|"
        skills_on_line = 0
        for skill_id, skill_emoji in skill_emojis.items():
            if skills_on_line >= skills_per_line:
                skills_on_line = 0
                value += "\n|"
            skill = next(
                filter(lambda s: s.skill_id == skill_id, self.player_profile.skills),
                None,
            )
            value += "{2}{0}{3}{1}{2}|".format(
                emoji_from_id(skill_emoji),
                pretty_format_skill_level(skill.get_level()),
                large_space,
                half_space,
            )
            skills_on_line += 1

        embed.add_field(name="Skills", value=value, inline=False)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return [heal_emoji_id]

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == heal_emoji_id:
            msg = hospital_service(self.player_profile)
            await self.embed_message.channel.send(msg)
            await self.update_embed_content()
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
