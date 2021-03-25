#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
import asyncio
from typing import List, Optional

from discord import Embed, User

from primerpg.data.boss_fight import BossFight
from primerpg.data.boss_profile import BossProfile
from primerpg.data.player_profile import PlayerProfile
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.boss_results_embed import BossResultsEmbed
from primerpg.embeds.common_embed import add_world_status_footer, add_detailed_stat_field
from primerpg.emojis import (
    emoji_from_id,
    letter_s_high_emoji_id,
    letter_a_high_emoji_id,
    letter_b_high_emoji_id,
    letter_c_high_emoji_id,
    letter_d_high_emoji_id,
    letter_f_high_emoji_id,
)
from primerpg.helpers.boss_helper import emoji_from_damage_type
from primerpg.helpers.player_helper import graduate_from_zone, save_player_profile
from primerpg.helpers.state_helper import set_player_state, idle_state_id
from primerpg.persistence.dto.move import Move
from primerpg.text_consts import no_space, horiz_bar, large_space, half_space

_emoji_list = [
    letter_s_high_emoji_id,
    letter_a_high_emoji_id,
    letter_b_high_emoji_id,
    letter_c_high_emoji_id,
    letter_d_high_emoji_id,
    letter_f_high_emoji_id,
]
_divider_bar_length = 20
_moves_per_line = 2
_log_actions_to_show = 6


class BossEmbed(BaseEmbed):
    def __init__(self, author: User, fighter_profile: PlayerProfile, enemy_profile: BossProfile):
        super().__init__(author)
        self.boss_fight = BossFight(fighter_profile, enemy_profile)
        self.move_emojis = []
        for i in range(0, len(self.boss_fight.player_moves)):
            self.move_emojis.append(_emoji_list[i])

    def generate_embed(self, *args) -> Embed:
        embed = Embed(
            title="Boss",
            description="{} is up against boss enemy {}.".format(
                self.boss_fight.player_profile.name, self.boss_fight.boss_profile.name
            ),
        )
        embed.set_thumbnail(url=self.boss_fight.boss_profile.get_icon_url())
        add_detailed_stat_field(
            embed,
            self.boss_fight.player_profile.name,
            self.boss_fight.player_profile,
            self.boss_fight.player_profile.core.zone_id,
            True,
        )
        add_detailed_stat_field(
            embed,
            self.boss_fight.boss_profile.name,
            self.boss_fight.boss_profile,
            self.boss_fight.player_profile.core.zone_id,
            True,
        )
        embed.add_field(name=horiz_bar * _divider_bar_length, value=no_space, inline=False)

        actions_text = ""
        name_length = max(map(lambda m: len(m.name), self.boss_fight.player_moves))
        move_number = 0
        for move in self.boss_fight.player_moves:
            move_emoji = emoji_from_id(self.move_emojis[move_number])
            type_emoji = emoji_from_damage_type(move.damage_type_id)
            name_text = move.name + (name_length - len(move.name)) * " "
            actions_text += "\n{2}{1}`{3}`{4}{0}-{0}{5}`{6}`{1}{7}`{8}`{0}".format(
                half_space,
                large_space,
                move_emoji,
                name_text,
                type_emoji,
                ":boom:",
                move.power,
                ":archery:",
                move.success_chance,
            )
            move_number += 1

        embed.add_field(name="Actions", value=actions_text, inline=False)

        log_text = ""
        for log_action in self.boss_fight.fight_log.get_last_actions(_log_actions_to_show):
            log_text += "\n" if log_action.newline and log_text else ""
            log_text += "{}".format(log_action.get_message())

        if log_text:
            embed.add_field(name=no_space, value=">>> {}".format(log_text), inline=False)

        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return self.move_emojis

    async def handle_fail_to_react(self):
        await self.take_turn_with_move(None)

    async def handle_reaction(self, reaction_id: int):
        # TODO Allow reactions by other players and allow other players to "buff" the currently fighting player,
        # TODO encouraging group play during boss fights
        if reaction_id in self.move_emojis:
            move = self.boss_fight.player_moves[self.move_emojis.index(reaction_id)]
            await self.embed_message.remove_reaction(emoji_from_id(reaction_id), self.author)
            await self.take_turn_with_move(move)
        else:
            await self.embed_message.channel.send("Failed to handle reaction")

    async def take_turn_with_move(self, move: Optional[Move]):
        self.boss_fight.take_full_turn(move)
        if self.boss_fight.is_fight_done():
            if self.boss_fight.boss_profile.is_dead():
                graduate_from_zone(self.boss_fight.player_profile, self.boss_fight.boss_profile.zone_id)
            await self.show_rewards_embed()
            # TODO Show new "Tutorial Embed" for zone
        else:
            loop = asyncio.get_event_loop()
            loop.create_task(self.update_embed_content())

    async def show_rewards_embed(self):
        embed = BossResultsEmbed(self.author, self.boss_fight)
        generated_embed = embed.generate_embed()
        if self.boss_fight.player_profile.is_dead():
            self.boss_fight.player_profile.heal_player_profile()
        save_player_profile(self.boss_fight.player_profile)
        set_player_state(self.boss_fight.player_profile.core.unique_id, idle_state_id)
        await self.embed_message.edit(embed=generated_embed)
        await embed.connect_reaction_listener(self.embed_message)
