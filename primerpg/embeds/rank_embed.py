#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import User, Embed

from primerpg.consts import overall_skill_id
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import pretty_format_with_length
from primerpg.emojis import skill_emojis, heal_emoji_id, emoji_from_id
from primerpg.helpers.player_helper import hospital_service, get_player_profile
from primerpg.persistence.player_rank_persistence import get_all_player_ranks
from primerpg.text_consts import large_space, half_space

_skills_per_line = 3


class RankEmbed(BaseEmbed):
    def __init__(self, player_id: int, author: User):
        super().__init__(author)
        self.player_profile = get_player_profile(player_id)
        self.player_ranks = get_all_player_ranks(player_id)
        self.author = author

    def generate_embed(self, recently_healed=False, *args) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Standings".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=self.author.avatar_url)
        if self.player_ranks:
            # TODO Associate emojis with rank
            overall_player_rank = next(
                filter(lambda pr: pr.skill_id == overall_skill_id, self.player_ranks),
                None,
            )
            embed.add_field(name="Global Rank", value="#{}".format(overall_player_rank.rank))
            value = "\n|"
            skills_on_line = 0
            max_rank_length = max(map(lambda pr: len("{}".format(pr.rank)), self.player_ranks))
            for skill in self.player_profile.skills:
                if skills_on_line >= _skills_per_line:
                    skills_on_line = 0
                    value += "\n|"
                if skill.get_total_xp() <= 0:
                    continue

                player_rank = next(
                    filter(lambda pr: pr.skill_id == skill.skill_id, self.player_ranks),
                    None,
                )
                if not player_rank:
                    continue

                skills_on_line += 1
                value += "{2}{0}{3}{1}{2}|".format(
                    emoji_from_id(skill_emojis[skill.skill_id]),
                    pretty_format_with_length(player_rank.rank, max_rank_length, "#"),
                    large_space,
                    half_space,
                )

            embed.add_field(name="Skill Ranks", value=value, inline=False)
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
