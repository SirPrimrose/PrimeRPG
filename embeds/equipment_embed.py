from typing import List

from discord import User, Embed

from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed
from emojis import (
    skill_emojis,
    grade_emojis,
)
from helpers.stat_helper import get_scaled_stat_value_for_item
from persistence.equipment_stat_persistence import get_equipment_stats
from text_consts import spaced_vert_line, horiz_bar
from urls import equipment_url
from util import (
    get_item_name,
    get_equipment_stat_category_name,
    get_key_for_value,
)

progress_bar_length = 20


class EquipmentEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__(author)
        self.player_profile = player_profile

    def generate_embed(self) -> Embed:
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
                cat_name = get_equipment_stat_category_name(
                    stat.equipment_stat_category_id
                )
                scaled_value = round(
                    get_scaled_stat_value_for_item(
                        equipment.item_id,
                        stat.equipment_stat_category_id,
                        self.player_profile.skills,
                    ),
                    1,
                )
                value += "\n**{}** - ({}) **{}**".format(
                    cat_name, stat.value, scaled_value
                )
                if len(stat.scales_with) > 0:
                    skill_line = "{}".format(spaced_vert_line)
                    scale_line = "{}".format(spaced_vert_line)
                    for skill_id, scaling in stat.scales_with.items():
                        skill_emoji = get_key_for_value(skill_emojis, skill_id)
                        skill_line += "{}{}".format(skill_emoji, spaced_vert_line)
                        scale_line += "{}{}".format(
                            get_scaling_grade(scaling), spaced_vert_line
                        )
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

    def get_reaction_emojis(self) -> List[str]:
        pass

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction):
        pass


def get_scaling_grade(scaling):
    for value, emoji in grade_emojis.items():
        if scaling <= value:
            return emoji
    return
