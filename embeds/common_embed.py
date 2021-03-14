from discord import Embed

from data.entity_base import EntityBase
from data.player_profile import PlayerProfile
from helpers.player_helper import heal_player_profile
from persistence.player_persistence import update_player_data
from text_consts import no_space


def add_detailed_stat_field(
    embed: Embed, field_title, profile: EntityBase, inline=False, recently_healed=False
):
    # TODO Find a better way to do things like "recently_healed" instead of passing in more arguments
    stats_value = "HP: {}/{}\nCombat Level: {}\nAttack: {}\nArmor: {}".format(
        profile.get_current_hp()
        if not recently_healed
        else "**{}**".format(profile.get_current_hp()),
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


def add_short_stat_field(embed: Embed, field_title, profile: EntityBase, inline=False):
    stats_value = "HP: {}/{}".format(
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


def heal_player(player_profile: PlayerProfile):
    heal_player_profile(player_profile)
    update_player_data(player_profile.core)


def pretty_format_skill_level(level: int) -> str:
    skill_level_text = "{}".format(level)
    return "`{}{}`".format((2 - len(skill_level_text)) * " ", skill_level_text)
