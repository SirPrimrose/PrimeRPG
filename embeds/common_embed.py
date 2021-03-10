import asyncio
from typing import List

from discord import Embed, User

from consts import game_client
from data.entity_base import EntityBase


def add_detailed_stat_field(
    embed: Embed, field_title, profile: EntityBase, inline=False
):
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


def add_short_stat_field(embed: Embed, field_title, profile: EntityBase, inline=False):
    stats_value = "HP: {}/{}".format(
        profile.current_hp,
        profile.get_max_hp(),
    )
    embed.add_field(
        name=field_title,
        value=stats_value,
        inline=inline,
    )


def get_reaction_check(embed_message, author: User, emoji_list: List[str]):
    def __reaction_check(reaction, user):
        if user != author and user != game_client.user:
            loop = asyncio.get_event_loop()
            loop.create_task(reaction.message.remove_reaction(reaction.emoji, user))
        return (
            user == author
            and reaction.message == embed_message
            and str(reaction.emoji) in emoji_list
        )

    return __reaction_check
