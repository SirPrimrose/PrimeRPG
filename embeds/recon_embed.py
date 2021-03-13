from typing import List

from discord import Embed, User

from consts import speed_skill_id
from data.entity_base import EntityBase
from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_detailed_stat_field, heal_player
from embeds.recon_results_embed import ReconResultsEmbed
from emojis import fight_emoji, heal_emoji, run_emoji
from helpers.battle_helper import get_flee_chance, sim_fight
from helpers.player_helper import save_player_profile, heal_player_profile
from util import get_current_in_game_time, get_current_in_game_weather


class ReconEmbed(BaseEmbed):
    def __init__(
        self, fighter_profile: PlayerProfile, enemy_profile: EntityBase, author: User
    ):
        super().__init__(author)
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile

    def generate_embed(self, recently_healed=False) -> Embed:
        # TODO Add random events into the recon action
        # TODO Randomly select an enemy to fight based on player area
        embed = Embed(
            description="{} did some recon and found a {}".format(
                self.fighter_profile.name, self.enemy_profile.name
            ),
        )
        embed.set_author(name="Recon", icon_url=self.fighter_profile.get_icon_url())
        embed.set_thumbnail(url=self.enemy_profile.get_icon_url())
        add_detailed_stat_field(
            embed,
            self.fighter_profile.name,
            self.fighter_profile,
            True,
            recently_healed,
        )
        add_detailed_stat_field(
            embed, self.enemy_profile.name, self.enemy_profile, True
        )
        fighter_speed = self.fighter_profile.get_skill_level(speed_skill_id)
        enemy_speed = self.enemy_profile.get_skill_level(speed_skill_id)
        flee_chance = get_flee_chance(fighter_speed, enemy_speed)
        action_text = "{} Fight\n{} Heal\n{} Run Away ({:.1f}%)".format(
            fight_emoji,
            heal_emoji,
            run_emoji,
            flee_chance * 100,
        )
        embed.add_field(name="Actions", value=action_text, inline=False)
        embed.set_footer(
            text="It is {} and {}".format(
                get_current_in_game_time(), get_current_in_game_weather()
            )
        )
        return embed

    def get_reaction_emojis(self) -> List[str]:
        return [
            fight_emoji,
            heal_emoji,
            run_emoji,
        ]

    async def handle_fail_to_react(self):
        await self.embed_message.channel.send("Failed to respond. Fighting...")
        await self.start_fight()

    async def handle_reaction(self, reaction):
        if str(reaction) == fight_emoji:
            await self.start_fight()
        elif str(reaction) == heal_emoji:
            heal_player(self.fighter_profile)
            await self.update_embed_content()
        elif str(reaction) == run_emoji:
            await self.embed_message.channel.send("Attempt to run")
        else:
            await self.embed_message.channel.send("Failed to handle reaction")

    async def start_fight(self):
        fight_log = sim_fight(self.fighter_profile, self.enemy_profile)
        embed = ReconResultsEmbed(
            self.fighter_profile, self.enemy_profile, fight_log, self.author
        )
        generated_embed = embed.generate_embed()
        if self.fighter_profile.is_dead():
            heal_player_profile(self.fighter_profile)
        save_player_profile(self.fighter_profile)
        await self.embed_message.edit(embed=generated_embed)
        await embed.connect_reaction_listener(self.embed_message)
