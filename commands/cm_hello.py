from typing import List

import discord

from commands.command import Command


class Hello(Command):
    def get_description(self):
        return "Say hi!"

    def get_name(self):
        return "Hello"

    def get_prefixes(self):
        return ["hello", "hi"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        if msg.author.nick:
            await msg.channel.send(
                "Hello {0.author.name}, or should I call you {0.author.nick}?".format(
                    msg
                )
            )
        else:
            await msg.channel.send(
                "Hello {0.author.name}... it seems that's all you go by.".format(msg)
            )
