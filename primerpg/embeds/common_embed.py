#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from math import floor

from discord import Embed

from primerpg.data.entity_base import EntityBase
from primerpg.text_consts import no_space
from primerpg.util import get_current_in_game_time, get_current_in_game_weather


def add_detailed_stat_field(embed: Embed, field_title, profile: EntityBase, inline=False, recently_healed=False):
    # TODO Find a better way to do things like "recently_healed" instead of passing in more arguments
    current_hp_text = format_hp(profile.get_current_hp(), recently_healed)
    stats_value = (
        "HP: {}/{:.0f}\nCombat Level: {}\nPhysical Attack: {}\nPhysical Armor: {}\nMagic Attack: {}\nMagic "
        "Armor: {}".format(
            current_hp_text,
            profile.get_max_hp(),
            profile.get_combat_level(),
            round(profile.get_phys_atk_power()),
            round(profile.get_phys_arm_power()),
            round(profile.get_mag_atk_power()),
            round(profile.get_mag_arm_power()),
        )
    )
    embed.add_field(
        name=field_title,
        value=stats_value,
        inline=inline,
    )


def add_short_stat_field(embed: Embed, field_title, profile: EntityBase, inline=False):
    stats_value = "HP: {:.0f}/{}".format(
        profile.get_current_hp(),
        profile.get_max_hp(),
    )
    embed.add_field(
        name=field_title,
        value=stats_value,
        inline=inline,
    )


def add_spacer_field(embed: Embed):
    embed.add_field(name=no_space, value=no_space, inline=False)


def add_world_status_footer(embed: Embed):
    embed.set_footer(text="It is {} and {}".format(get_current_in_game_time(), get_current_in_game_weather()))


def pretty_format_skill_level(level: int) -> str:
    skill_level_text = "{}".format(level)
    return "`{}{}`".format((2 - len(skill_level_text)) * " ", skill_level_text)


def format_hp(hp: float, bold: bool = False) -> str:
    if 0 < hp < 1:
        hp = 1.0
    return "{:.0f}".format(hp) if not bold else "**{:.0f}**".format(hp)
