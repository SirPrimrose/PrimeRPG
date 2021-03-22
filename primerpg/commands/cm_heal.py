#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.helpers.player_helper import (
    get_player_profile,
    hospital_service,
)


class Heal(Command):
    def get_description(self):
        return "Heal yourself."

    def get_name(self):
        return "Heal"

    def get_prefixes(self):
        return ["heal"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        message = hospital_service(player_profile)
        await msg.channel.send(message)
