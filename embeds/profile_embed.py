import asyncio

from discord import User, Embed, Message

from consts import game_client
from data.player_profile import PlayerProfile
from embeds.base_embed import BaseEmbed
from embeds.common_embed import (
    add_detailed_stat_field,
    get_reaction_check,
    pretty_format_skill_level,
)
from emojis import skill_emojis, heal_emoji
from text_consts import large_space, small_space
from urls import profile_url

skills_per_line = 3


class ProfileEmbed(BaseEmbed):
    def __init__(self, player_profile: PlayerProfile, author: User):
        super().__init__(author)
        self.player_profile = player_profile
        self.author = author

    def generate_embed(self) -> Embed:
        embed = Embed()
        embed.set_author(
            name="{}'s Profile".format(self.author.name),
            icon_url=self.author.avatar_url,
        )
        embed.set_thumbnail(url=profile_url)
        add_detailed_stat_field(embed, "Stats", self.player_profile)
        value = "\n|"
        skills_on_line = 0
        for skill_emoji, skill_id in skill_emojis.items():
            if skills_on_line >= skills_per_line:
                skills_on_line = 0
                value += "\n|"
            skill = next(
                filter(lambda s: s.skill_id == skill_id, self.player_profile.skills),
                None,
            )
            value += "{2}{0}{3}{1}{2}|".format(
                skill_emoji,
                pretty_format_skill_level(skill.get_level()),
                large_space,
                small_space,
            )
            skills_on_line += 1

        embed.add_field(name="Skills", value=value, inline=False)
        return embed

    async def connect_reaction_listener(self, embed_message: Message) -> None:
        self.embed_message = embed_message
        await asyncio.gather(
            self.embed_message.add_reaction(heal_emoji),
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
                        heal_emoji,
                    ],
                ),
            )
        except asyncio.TimeoutError:
            pass
        else:
            await self.handle_reaction(reaction)

    async def handle_reaction(self, reaction):
        if str(reaction) == heal_emoji:
            await self.embed_message.channel.send("Attempt to heal")
        else:
            await self.embed_message.channel.send("Failed to handle reaction")
