#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import Embed, User

from primerpg.data.entity_base import EntityBase
from primerpg.data.fight_log.fight_log import FightLog
from primerpg.data.player_profile import PlayerProfile
from primerpg.data_cache import get_item_name
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_detailed_stat_field, add_spacer_field
from primerpg.emojis import skill_emojis, info_emoji_id, heal_emoji_id, emoji_from_id
from primerpg.helpers.log_helper import print_log
from primerpg.helpers.player_helper import hospital_service
from primerpg.text_consts import no_space, half_space


class ReconResultsEmbed(BaseEmbed):
    def __init__(
        self,
        author: User,
        fighter_profile: PlayerProfile,
        enemy_profile: EntityBase,
        fight_log: FightLog,
    ):
        super().__init__(author)
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile
        self.fight_log = fight_log

    def generate_embed(self, recently_healed=False, *args) -> Embed:
        winner = self.enemy_profile.name if self.fighter_profile.is_dead() else self.fighter_profile.name
        loser = self.fighter_profile.name if self.fighter_profile.is_dead() else self.enemy_profile.name
        embed = Embed(title="Recon Results", description="{} defeated {}".format(winner, loser))
        embed.set_thumbnail(url=self.enemy_profile.get_icon_url())
        add_detailed_stat_field(
            embed,
            self.fighter_profile.name,
            self.fighter_profile,
            self.fighter_profile.core.zone_id,
            True,
            recently_healed,
        )
        add_detailed_stat_field(
            embed, self.enemy_profile.name, self.enemy_profile, self.fighter_profile.core.zone_id, True
        )

        if winner == self.fighter_profile.name:
            # Calculate item drop and effort text fields
            item_drops_text = ""
            for reward in self.fight_log.get_rewards():
                if reward.quantity > 0:
                    item_name = get_item_name(reward.item_id)
                    item_drops_text += "\n{}: {}".format(item_name, reward.quantity)
            effort_text = ""
            for effort in self.fight_log.get_efforts():
                if effort.value > 0:
                    skill_emoji = skill_emojis[effort.skill_id]
                    effort_text += "\n{}{}{}".format(emoji_from_id(skill_emoji), half_space, effort.value)

            # Spacer field so inlines do not overlap
            if item_drops_text or effort_text:
                add_spacer_field(embed)
            if item_drops_text:
                embed.add_field(
                    name="Drops",
                    value=item_drops_text if item_drops_text else no_space,
                    inline=True,
                )
            if effort_text:
                embed.add_field(
                    name="Efforts",
                    value=effort_text if effort_text else no_space,
                    inline=True,
                )
        else:
            embed.add_field(
                name="Death",
                value="{} has died. Receive no rewards from the fight and potentially lose xp in all skills. See "
                "combat log for more info.".format(self.fighter_profile.name),
                inline=False,
            )
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return [info_emoji_id, heal_emoji_id]

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == info_emoji_id:
            await print_log(self.embed_message.channel, self.fight_log)
        elif reaction_id == heal_emoji_id:
            msg = hospital_service(self.fighter_profile)
            await self.embed_message.channel.send(msg)
            await self.update_embed_content()
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
