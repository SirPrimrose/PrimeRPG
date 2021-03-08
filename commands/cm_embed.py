from typing import List

import discord

from commands.command import Command
import emojis


class EmbedCommand(Command):
    def get_description(self):
        return "Get a test embed."

    def get_name(self):
        return "Embed"

    def get_prefixes(self):
        return ["embed"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        embed = discord.Embed(title="Title Here")
        embed.add_field(
            name="Example", value="Text {}".format(emojis.triumph_emoji), inline=False
        )
        await msg.channel.send(embed=embed)
