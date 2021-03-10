from discord import Embed

from data.entity_base import EntityBase
from embeds.base_embed import BaseEmbed
from embeds.common_embed import add_stat_field
from text_consts import no_space


class ReconEmbed(BaseEmbed):
    def __init__(self, fighter_profile: EntityBase, enemy_profile: EntityBase):
        super().__init__()
        self.fighter_profile = fighter_profile
        self.enemy_profile = enemy_profile

    def generate_embed(self) -> Embed:
        embed = Embed(
            title="Fight Status",
            description="{} did some recon and fought a {}".format(
                self.fighter_profile.name, self.enemy_profile.name
            ),
        )
        embed.set_thumbnail(url=self.enemy_profile.get_icon_url())
        embed.add_field(name="Ending Stats", value=no_space, inline=False)
        add_stat_field(embed, self.fighter_profile.name, self.fighter_profile, True)
        add_stat_field(embed, self.enemy_profile.name, self.enemy_profile, True)
        embed.add_field(name="Rewards", value="Gold: 5", inline=False)
        return embed
