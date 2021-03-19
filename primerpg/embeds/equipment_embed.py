#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import User, Embed

from primerpg.data.player_profile import PlayerProfile
from primerpg.data_cache import get_equipment_stat_category_name, get_item_name
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.emojis import (
    skill_emojis,
    grade_emojis,
    emoji_from_id,
)
from primerpg.helpers.stat_helper import get_scaled_stat_value_for_item
from primerpg.persistence.equipment_stat_persistence import get_equipment_stats
from primerpg.text_consts import spaced_vert_line, horiz_bar
from primerpg.urls import equipment_url
from primerpg.util import (
    get_key_for_value,
)

progress_bar_length = 20


class EquipmentEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__(author)
        self.player_profile = player_profile

    def generate_embed(self, *args) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Equipment".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=equipment_url)
        for equipment in self.player_profile.equipment:
            stats = get_equipment_stats(equipment.item_id)
            value = ""
            for stat in stats:
                cat_name = get_equipment_stat_category_name(stat.equipment_stat_category_id)
                scaled_value = round(
                    get_scaled_stat_value_for_item(
                        equipment.item_id,
                        stat.equipment_stat_category_id,
                        self.player_profile.skills,
                    ),
                    1,
                )
                value += "\n**{}** - ({}) **{}**".format(cat_name, stat.value, scaled_value)
                if len(stat.scales_with) > 0:
                    skill_line = "{}".format(spaced_vert_line)
                    scale_line = "{}".format(spaced_vert_line)
                    for skill_id, scaling in stat.scales_with.items():
                        skill_emoji = get_key_for_value(skill_emojis, skill_id)
                        skill_line += "{}{}".format(emoji_from_id(skill_emoji), spaced_vert_line)
                        scale_line += "{}{}".format(get_scaling_grade(scaling), spaced_vert_line)
                    scaling_table = "{}\n{}".format(skill_line, scale_line)
                    value += "\nStat Bonus:\n{}".format(scaling_table)
            value += "\n" + horiz_bar * 15
            embed.add_field(
                name=get_item_name(equipment.item_id),
                value=value,
                inline=False,
            )
        print(len(embed))
        return embed

    def get_reaction_emojis(self) -> List[int]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        pass


def get_scaling_grade(scaling):
    for value, emoji in grade_emojis.items():
        if scaling <= value:
            return emoji
    return
