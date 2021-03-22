#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.data_cache import get_item_id
from primerpg.helpers.item_helper import attempt_use_item
from primerpg.helpers.player_helper import get_player_profile, save_player_profile
from primerpg.util import check_is_int


class Use(Command):
    def get_description(self):
        return "Uses an item."

    def get_name(self):
        return "Use"

    def get_prefixes(self):
        return ["use"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        try:
            use_count = 1
            item_name = ""
            for arg in args:
                if check_is_int(arg):
                    use_count = int(arg)
                    break
                else:
                    item_name += "{} ".format(arg)
            item_name = item_name.strip()
            item_id = get_item_id(item_name)
            if item_id:
                profile = get_player_profile(msg.author.id)
                success, message = attempt_use_item(profile, item_id, use_count)
                if success:
                    save_player_profile(profile)
                await msg.channel.send(message)
            else:
                await msg.channel.send("Item not found.")
        except ValueError:
            await msg.channel.send("Enter an item name to use.")
