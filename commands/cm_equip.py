from typing import List

import discord

from commands.command import Command
from helpers.equipment_helper import equip_player_item
from helpers.player_helper import get_player_profile, save_player_profile
from util import get_item_id


class Equip(Command):
    def get_description(self):
        return "Equips the given item."

    def get_name(self):
        return "Equip"

    def get_prefixes(self):
        return ["equip", "eq"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_profile = get_player_profile(player_id)
        # TODO Make this response an embed that allows showing the updated equipment embed
        item_id = get_item_id(" ".join(args))
        if item_id:
            response = equip_player_item(player_profile, item_id)
            save_player_profile(player_profile)
            await msg.channel.send("Equip success." if not response else response)
        else:
            await msg.channel.send("Enter a valid item name.")
