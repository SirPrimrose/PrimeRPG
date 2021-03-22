#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import Embed, User

from primerpg.consts import speed_skill_id
from primerpg.data.entity_base import EntityBase
from primerpg.data.player_profile import PlayerProfile
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.embeds.common_embed import add_detailed_stat_field, heal_player, add_world_status_footer
from primerpg.embeds.recon_results_embed import ReconResultsEmbed
from primerpg.emojis import (
    fight_emoji_id,
    heal_emoji_id,
    run_emoji_id,
    emoji_from_id,
)
from primerpg.helpers.battle_helper import get_flee_chance, sim_fight
from primerpg.helpers.player_helper import save_player_profile, hospital_service
from primerpg.helpers.state_helper import set_player_state, idle_state_id


class ReconEmbed(BaseEmbed):
    def __init__(self, fighter_profile: PlayerProfile, enemy_profile: EntityBase, author: User):
        super().__init__(author)
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile
        # TODO Randomly select an enemy to fight based on player area

    def generate_embed(self, recently_healed=False, *args) -> Embed:
        # TODO Add random events into the recon action
        embed = Embed(
            title="Recon",
            description="{} did some recon and found a {}".format(self.fighter_profile.name, self.enemy_profile.name),
        )
        embed.set_thumbnail(url=self.enemy_profile.get_icon_url())
        add_detailed_stat_field(
            embed,
            self.fighter_profile.name,
            self.fighter_profile,
            True,
            recently_healed,
        )
        add_detailed_stat_field(embed, self.enemy_profile.name, self.enemy_profile, True)
        fighter_speed = self.fighter_profile.get_skill_level(speed_skill_id)
        enemy_speed = self.enemy_profile.get_skill_level(speed_skill_id)
        flee_chance = get_flee_chance(fighter_speed, enemy_speed)
        action_text = "{} Fight\n{} Heal\n{} Run Away ({:.1f}%)".format(
            emoji_from_id(fight_emoji_id),
            emoji_from_id(heal_emoji_id),
            emoji_from_id(run_emoji_id),
            flee_chance * 100,
        )
        embed.add_field(name="Actions", value=action_text, inline=False)
        add_world_status_footer(embed)
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return [
            fight_emoji_id,
            heal_emoji_id,
            run_emoji_id,
        ]

    async def handle_fail_to_react(self):
        await self.embed_message.channel.send("Failed to respond. Fighting...")
        await self.start_fight()

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == fight_emoji_id:
            await self.start_fight()
        elif reaction_id == heal_emoji_id:
            msg = hospital_service(self.fighter_profile)
            await self.embed_message.channel.send(msg)
            await self.update_embed_content()
        elif reaction_id == run_emoji_id:
            await self.embed_message.channel.send("Run success")
            set_player_state(self.fighter_profile.core.unique_id, idle_state_id)
        else:
            await self.embed_message.channel.send("Failed to handle reaction")

    async def start_fight(self):
        fight_log = sim_fight(self.fighter_profile, self.enemy_profile)
        embed = ReconResultsEmbed(self.fighter_profile, self.enemy_profile, fight_log, self.author)
        generated_embed = embed.generate_embed()
        if self.fighter_profile.is_dead():
            self.fighter_profile.heal_player_profile()
        save_player_profile(self.fighter_profile)
        set_player_state(self.fighter_profile.core.unique_id, idle_state_id)
        await self.embed_message.edit(embed=generated_embed)
        await embed.connect_reaction_listener(self.embed_message)
