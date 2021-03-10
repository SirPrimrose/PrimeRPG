from discord import Embed

from data.entity_base import EntityBase
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_short_stat_field


class ReconResultsEmbed(BaseEmbed):
    def __init__(self, fighter_profile: EntityBase, enemy_profile: EntityBase):
        super().__init__()
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile

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
