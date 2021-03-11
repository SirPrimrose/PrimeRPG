import asyncio

from discord import Embed, Message, User

from consts import speed_skill_id, game_client
from data.entity_base import EntityBase
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_detailed_stat_field, get_reaction_check
from embeds.recon_results_embed import ReconResultsEmbed
from emojis import fight_emoji, heal_emoji, run_emoji
from helpers.battle_helper import get_flee_chance, sim_fight
from text_consts import no_space
from util import get_current_in_game_time, get_current_in_game_weather


class ReconEmbed(BaseEmbed):
    def __init__(
        self,
        fighter_profile: EntityBase,
        enemy_profile: EntityBase,
        embed_message: Message = None,
        author=None,
    ):
        super().__init__()
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile
        self.embed_message = embed_message
        self.author = author

    def generate_embed(self) -> Embed:
        # TODO Add random events into the recon action
        # TODO Randomly select an enemy to fight based on player area
        embed = Embed(
            title="Recon",
            description="{} did some recon and found a {}".format(
                self.fighter_profile.name, self.enemy_profile.name
            ),
        )
        embed.set_author(name=no_space, icon_url=self.fighter_profile.get_icon_url())
        embed.set_thumbnail(url=self.enemy_profile.get_icon_url())
        add_detailed_stat_field(
            embed, self.fighter_profile.name, self.fighter_profile, True
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

    async def connect_reaction_listener(
        self, embed_message: Message, author: User
    ) -> None:
        self.embed_message = embed_message
        self.author = author
        await asyncio.gather(
            self.embed_message.add_reaction(fight_emoji),
            self.embed_message.add_reaction(heal_emoji),
            self.embed_message.add_reaction(run_emoji),
            self.listen_for_reaction(),
        )

    async def listen_for_reaction(self):
        try:
            reaction, user = await game_client.wait_for(
                "reaction_add",
                timeout=60.0,
                check=get_reaction_check(
                    self.embed_message,
                    self.author,
                    [
                        fight_emoji,
                        heal_emoji,
                        run_emoji,
                    ],
                ),
            )
        except asyncio.TimeoutError:
            await self.embed_message.channel.send("Failed to respond. Fighting...")
            await self.start_fight()
        else:
            await self.handle_reaction(reaction)

    async def handle_reaction(self, reaction):
        if str(reaction) == fight_emoji:
            await self.start_fight()
        elif str(reaction) == heal_emoji:
            await self.embed_message.channel.send("Attempt to heal")
        elif str(reaction) == run_emoji:
            await self.embed_message.channel.send("Attempt to run")
        else:
            await self.embed_message.channel.send("Failed to handle reaction")

    async def start_fight(self):
        fight_log = sim_fight(self.fighter_profile, self.enemy_profile)
        embed = ReconResultsEmbed(self.fighter_profile, self.enemy_profile, fight_log)
        msg = await self.embed_message.channel.send(embed=embed.generate_embed())
        await embed.connect_reaction_listener(msg, self.author)
