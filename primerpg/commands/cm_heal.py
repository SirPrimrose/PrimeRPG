#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.helpers.item_helper import attempt_use_item
from primerpg.helpers.player_helper import (
    get_player_profile,
    save_player_profile,
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
        success = attempt_use_item(player_profile, 101)
        # TODO Format message based on item id and effect
        if success:
            save_player_profile(player_profile)
            await msg.channel.send("Used a bandage and healed {}".format(msg.author.name))
        else:
            await msg.channel.send("{} has no bandages".format(msg.author.name))
