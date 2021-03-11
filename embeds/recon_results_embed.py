import asyncio

from discord import Embed, Message, User

from consts import game_client
from data.entity_base import EntityBase
from data.fight_log.fight_log import FightLog
from data.fight_log.turn_action import TurnAction
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_short_stat_field, get_reaction_check
from emojis import info_emoji


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

    def generate_embed(self) -> Embed:
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
        add_short_stat_field(
            embed, self.fighter_profile.name, self.fighter_profile, True
        )
        add_short_stat_field(embed, self.enemy_profile.name, self.enemy_profile, True)
        embed.add_field(name="Rewards", value="Gold: 5", inline=False)
        return embed

    async def connect_reaction_listener(self, embed_message: Message) -> None:
        self.embed_message = embed_message
        await asyncio.gather(
            self.embed_message.add_reaction(info_emoji),
            self.listen_for_reaction(),
        )

    async def listen_for_reaction(self):
        try:
            reaction, user = await game_client.wait_for(
                "reaction_add",
                timeout=60.0,
                check=get_reaction_check(self.embed_message, self.author, [info_emoji]),
            )
        except asyncio.TimeoutError:
            pass
        else:
            await self.handle_reaction(reaction)

    async def handle_reaction(self, reaction):
        if str(reaction) == info_emoji:
            await self.print_log()
        else:
            await self.embed_message.channel.send("Failed to handle reaction")

    async def print_log(self):
        response = ""
        current_turn = ""

        async def check_add_turn_to_response():
            nonlocal response, current_turn
            if len(response) + len(current_turn) >= 2000:
                await self.embed_message.channel.send(response)
                response = ""
            response += current_turn
            current_turn = ""

        for log in self.fight_log.actions:
            if type(log) == TurnAction:
                await check_add_turn_to_response()
            current_turn += "{}\n".format(log.get_message())
        await check_add_turn_to_response()

        await self.embed_message.channel.send(response)
