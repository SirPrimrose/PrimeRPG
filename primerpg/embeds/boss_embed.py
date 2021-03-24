#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
import asyncio
from typing import List

from discord import Embed, User

from primerpg.data.boss_fight import BossFight
from primerpg.data.boss_profile import BossProfile
from primerpg.data.player_profile import PlayerProfile
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_world_status_footer
from primerpg.emojis import (
    emoji_from_id,
    letter_s_high_emoji_id,
    letter_a_high_emoji_id,
    letter_b_high_emoji_id,
    letter_c_high_emoji_id,
    letter_d_high_emoji_id,
    letter_f_high_emoji_id,
)
from primerpg.text_consts import no_space, horiz_bar, large_space

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
        for i in range(0, len(self.boss_fight.fighter_moves)):
            self.move_emojis.append(_emoji_list[i])

    def generate_embed(self, *args) -> Embed:
        embed = Embed(
            title="Boss",
            description="{} is up against boss enemy {}.".format(
                self.boss_fight.player_profile.name, self.boss_fight.boss_profile.name
            ),
        )
        embed.set_thumbnail(url=self.boss_fight.boss_profile.get_icon_url())
        embed.add_field(name="Player Stats", value="HP: {}".format(self.boss_fight.player_profile.get_current_hp()))
        embed.add_field(name="Boss Stats", value="HP: {}".format(self.boss_fight.boss_profile.get_current_hp()))
        embed.add_field(name=horiz_bar * _divider_bar_length, value=no_space, inline=False)

        actions_text = "\n|"
        name_length = max(map(lambda m: len(m.name), self.boss_fight.fighter_moves))
        moves_on_line = 0
        move_number = 0
        for move in self.boss_fight.fighter_moves:
            if moves_on_line >= _moves_per_line:
                moves_on_line = 0
                actions_text += "\n|"
            move_emoji = emoji_from_id(self.move_emojis[move_number])
            name_text = move.name + (name_length - len(move.name)) * " "
            actions_text += "{2}{0}{2}`{1}`{2}|".format(move_emoji, name_text, large_space)
            moves_on_line += 1
            move_number += 1

        embed.add_field(name="Actions", value=actions_text, inline=False)

        log_text = ""
        for log_action in self.boss_fight.log.get_last_actions(_log_actions_to_show):
            log_text += "{}\n".format(log_action.get_message())

        if log_text:
            embed.add_field(name=no_space, value=">>> {}".format(log_text), inline=False)

        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return self.move_emojis

    async def handle_fail_to_react(self):
        await self.embed_message.channel.send("Failed to respond. Choosing random move...")

    async def handle_reaction(self, reaction_id: int):
        if reaction_id in self.move_emojis:
            move = self.boss_fight.fighter_moves[self.move_emojis.index(reaction_id)]
            self.boss_fight.take_full_turn(move)
            await self.embed_message.remove_reaction(emoji_from_id(reaction_id), self.author)
            loop = asyncio.get_event_loop()
            loop.create_task(self.update_embed_content())
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
