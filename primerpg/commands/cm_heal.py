#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.helpers.player_helper import (
    get_player_profile,
    save_player_profile,
    heal_player_profile,
)


class Heal(Command):
    def get_description(self):
        return "Heal a player."

    def get_name(self):
        return "Heal"

    def get_prefixes(self):
        return ["heal"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        heal_player_profile(player_profile)
        save_player_profile(player_profile)
        await msg.channel.send("Healed {}".format(msg.author.name))
