#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.data_cache import get_item_id
from primerpg.helpers.equipment_helper import unequip_player_item
from primerpg.helpers.player_helper import get_player_profile, save_player_profile


class Unequip(Command):
    def get_description(self):
        return "Unequips the given item."

    def get_name(self):
        return "Unequip"

    def get_prefixes(self):
        return ["unequip", "uneq"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        # TODO Make this response an embed that allows showing the updated equipment embed
        item_id = get_item_id(" ".join(args))
        if item_id:
            response = unequip_player_item(player_profile, item_id)
            save_player_profile(player_profile)
            await msg.channel.send("Unequip success." if not response else response)
        else:
            await msg.channel.send("Enter a valid item name.")
