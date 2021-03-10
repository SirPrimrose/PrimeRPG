from discord import Embed

from data.entity_base import EntityBase


def add_stat_field(embed: Embed, field_title, profile: EntityBase, inline=False):
    stats_value = "HP: {}/{}\nCombat Level: {}\nAttack: {}\nArmor: {}".format(
        profile.current_hp,
        profile.get_max_hp(),
        profile.get_combat_level(),
        profile.get_attack_power(),
        profile.get_armor_power(),
    )
    embed.add_field(
        name=field_title,
        value=stats_value,
        inline=inline,
    )
