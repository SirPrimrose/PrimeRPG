#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import User, Embed

from primerpg.consts import overall_skill_id
from primerpg.data.player_profile import PlayerProfile
from primerpg.data_cache import get_zone_name, get_equipment_category_name, get_item_name
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_detailed_stat_field, pretty_format_with_length
from primerpg.emojis import skill_emojis, heal_emoji_id, emoji_from_id
from primerpg.helpers.player_helper import hospital_service
from primerpg.persistence.player_rank_persistence import get_player_rank
from primerpg.text_consts import large_space, half_space
from primerpg.urls import profile_url

_skills_per_line = 3


class ProfileEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__(author)
        self.player_profile = player_profile
        self.author = author
        self.player_rank = get_player_rank(player_profile.core.unique_id, overall_skill_id)

    def generate_embed(self, recently_healed=False, *args) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Profile".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=profile_url)
        embed.add_field(name="Zone", value="{}".format(get_zone_name(self.player_profile.core.zone_id)))
        add_detailed_stat_field(
            embed, "Stats", self.player_profile, self.player_profile.core.zone_id, recently_healed=recently_healed
        )
        value = "\n|"
        skills_on_line = 0
        for skill_id, skill_emoji in skill_emojis.items():
            if skills_on_line >= _skills_per_line:
                skills_on_line = 0
                value += "\n|"
            skill = next(
                filter(lambda s: s.skill_id == skill_id, self.player_profile.skills),
                None,
            )
            if skill.get_total_xp() <= 0:
                continue
            value += "{2}{0}{3}{1}{2}|".format(
                emoji_from_id(skill_emoji),
                pretty_format_with_length(skill.get_level(), 2),
                large_space,
                half_space,
            )
            skills_on_line += 1

        embed.add_field(name="Skills", value=value, inline=False)

        equipment_text = ""
        for equipment in self.player_profile.equipment:
            category_name = get_equipment_category_name(equipment.equipment_category_id)
            item_name = get_item_name(equipment.item_id)
            equipment_text += "**{}** - {}\n".format(category_name, item_name)
        embed.add_field(
            name="Equipment",
            value=equipment_text,
            inline=False,
        )
        if self.player_rank:
            embed.set_footer(text="Rank #{}".format(self.player_rank.rank))
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
