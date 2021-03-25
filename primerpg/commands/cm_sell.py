#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.data_cache import get_item_id
from primerpg.embeds.simple_embed import SimpleEmbed
from primerpg.helpers.item_helper import attempt_sell_item
from primerpg.helpers.player_helper import get_player_profile, save_player_profile
from primerpg.persistence.items_persistence import get_item
from primerpg.util import check_is_int


class Sell(Command):
    def get_description(self):
        return "Sell an item."

    def get_name(self):
        return "Sell"

    def get_prefixes(self):
        return ["sell", "s"]

    async def run_command(self, msg: discord.Message, args: List[str]):
        try:
            purchase_count = 1
            item_name = ""
            for arg in args:
                if check_is_int(arg):
                    purchase_count = int(arg)
                    break
                else:
                    item_name += "{} ".format(arg)
            item_name = item_name.strip()
            item_id = get_item_id(item_name)
            if item_id:
                shop_item = get_item(item_id)
                profile = get_player_profile(msg.author.id)
                transaction = attempt_sell_item(profile, shop_item, purchase_count)
                save_player_profile(profile)
                if transaction.err_message:
                    title = "Failed to sell {}".format(shop_item.name)
                    content = transaction.err_message
                else:
                    title = "Sell success"
                    content = "{0} sold {1.quantity} {1.item.name} for {1.total_cost} coins".format(
                        msg.author.name, transaction
                    )
                embed = SimpleEmbed(msg.author, title, content)
                await msg.channel.send(embed=embed.generate_embed())
            else:
                await msg.channel.send("Item not found.")
        except ValueError:
            await msg.channel.send("Enter an item name to use.")
