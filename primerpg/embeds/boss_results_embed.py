#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from discord import Embed, User

from primerpg.data.boss_fight import BossFight
from primerpg.embeds.base_embed import BaseEmbed
from primerpg.emojis import info_emoji_id, heal_emoji_id
from primerpg.helpers.log_helper import print_log
from primerpg.helpers.player_helper import hospital_service


class BossResultsEmbed(BaseEmbed):
    def __init__(self, author: User, boss_fight: BossFight):
        super().__init__(author)
        self.boss_fight = boss_fight

    def generate_embed(self, recently_healed=False, *args) -> Embed:
        player = self.boss_fight.player_profile
        boss = self.boss_fight.boss_profile
        winner = boss.name if player.is_dead() else player.name
        loser = player.name if player.is_dead() else boss.name
        embed = Embed(title="Boss Results", description="{} defeated {}".format(winner, loser))
        embed.set_thumbnail(url=boss.get_icon_url())

        if winner == player.name:
            embed.add_field(
                name="Success",
                value="You have defeated the boss and are granted access to a new zone. New commands have been "
                "unlocked and new enemies are available to fight.",
            )
        else:
            embed.add_field(
                name="Death",
                value="{} has died. Receive no rewards from the fight and potentially lose xp in all skills. See "
                "combat log for more info.".format(player.name),
                inline=False,
            )
        return embed

    def get_reaction_emojis(self) -> List[int]:
        return [info_emoji_id, heal_emoji_id]

    async def handle_fail_to_react(self):
        pass

    async def handle_reaction(self, reaction_id: int):
        if reaction_id == info_emoji_id:
            await print_log(self.embed_message.channel, self.boss_fight.fight_log)
        elif reaction_id == heal_emoji_id:
            msg = hospital_service(self.boss_fight.player_profile)
            await self.embed_message.channel.send(msg)
            await self.update_embed_content()
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
