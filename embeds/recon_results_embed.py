from typing import List

from discord import Embed, User

from data.entity_base import EntityBase
from data.fight_log.fight_log import FightLog
from data.fight_log.turn_action import TurnAction
from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_detailed_stat_field, heal_player, add_spacer_field
from embeds.simple_embed import SimpleEmbed
from emojis import skill_emojis, info_emoji_id, heal_emoji_id, emoji_from_id
from persistence.items_persistence import get_item
from text_consts import no_space, half_space
from util import get_key_for_value


class ReconResultsEmbed(BaseEmbed):
    def __init__(
        self,
        fighter_profile: PlayerProfile,
        enemy_profile: EntityBase,
        fight_log: FightLog,
        author: User,
    ):
        super().__init__(author)
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile
        self.fight_log = fight_log

    def generate_embed(self, recently_healed=False) -> Embed:
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
        embed = Embed(
            title="Recon Results", description="{} defeated {}".format(winner, loser)
        )
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

        # Calculate item drop and effort text fields
        item_drops_text = ""
        for reward in self.fight_log.get_rewards():
            item_name = get_item(reward.item_id).name
            item_drops_text += "\n{}: {}".format(item_name, reward.quantity)
        effort_text = ""
        for effort in self.fight_log.efforts:
            skill_emoji = get_key_for_value(skill_emojis, effort.skill_id)
            effort_text += "\n{}{}{}".format(
                emoji_from_id(skill_emoji), half_space, effort.value
            )

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
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return [info_emoji_id, heal_emoji_id]

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == info_emoji_id:
            await self.print_log()
        elif reaction_id == heal_emoji_id:
            heal_player(self.fighter_profile)
            await self.update_embed_content()
        else:
            await self.embed_message.channel.send("Failed to handle reaction")

    async def print_log(self):
        response = ""
        current_turn = ""
        page_num = 1

        async def check_add_turn_to_response():
            nonlocal response, current_turn, page_num
            if len(response) + len(current_turn) >= 2048:
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
