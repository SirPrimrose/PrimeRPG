from typing import List

from discord import Embed, User

from data.entity_base import EntityBase
from data.fight_log.fight_log import FightLog
from data.fight_log.turn_action import TurnAction
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_short_stat_field, add_detailed_stat_field
from embeds.simple_embed import SimpleEmbed
from emojis import info_emoji, heal_emoji
from helpers.player_helper import heal_player_profile


class ReconResultsEmbed(BaseEmbed):
    def __init__(
        self,
        fighter_profile: EntityBase,
        enemy_profile: EntityBase,
        fight_log: FightLog,
        author: User,
    ):
        super().__init__(author)
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile
        self.fight_log = fight_log

    def generate_embed(self, recently_healed=False) -> Embed:
        embed = Embed()
        embed.set_thumbnail(url=self.enemy_profile.get_icon_url())
        winner = (
            self.enemy_profile.name
            if self.fighter_profile.is_dead()
            else self.fighter_profile.name
        )
        loser = (
            self.fighter_profile.name
            if self.fighter_profile.is_dead()
            else self.enemy_profile.name
        )
        embed.add_field(
            name="Summary", value="{} defeated {}".format(winner, loser), inline=False
        )
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
        embed.add_field(name="Rewards", value="Gold: 5", inline=False)
        return embed

    def get_reaction_emojis(self) -> List[str]:
        return [info_emoji, heal_emoji]

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction):
        if str(reaction) == info_emoji:
            await self.print_log()
        elif str(reaction) == heal_emoji:
            heal_player_profile(self.fighter_profile)
            await self.update_embed_content()
        else:
            await self.embed_message.channel.send("Failed to handle reaction")

    async def print_log(self):
        response = ""
        current_turn = ""
        page_num = 1

        async def check_add_turn_to_response():
            nonlocal response, current_turn, page_num
            if len(response) + len(current_turn) >= 2000:
                await self.send_fight_log_page(page_num, response)
                page_num += 1
                response = ""
            response += current_turn
            current_turn = ""

        for log in self.fight_log.actions:
            if type(log) == TurnAction:
                await check_add_turn_to_response()
            current_turn += "\n" if log.newline else ""
            current_turn += "{}".format(log.get_message())
        await check_add_turn_to_response()

        await self.send_fight_log_page(page_num, response, page_num != 1)

    async def send_fight_log_page(self, page_num, content, show_page_num=True):
        title = "Fight Log Page {}".format(page_num) if show_page_num else "Fight Log"
        embed = SimpleEmbed(self.author, title, content)
        await self.embed_message.channel.send(embed=embed.generate_embed())
