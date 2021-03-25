#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

import discord

from primerpg.commands.command import Command
from primerpg.data_cache import get_item_id
from primerpg.embeds.purchase_result_embed import PurchaseResultEmbed
from primerpg.embeds.simple_embed import SimpleEmbed
from primerpg.helpers.item_helper import attempt_purchase_item
from primerpg.helpers.player_helper import get_player_profile, save_player_profile
from primerpg.persistence.items_persistence import get_item
from primerpg.util import check_is_int


class Buy(Command):
    def get_description(self):
        return "Buy an item."

    def get_name(self):
        return "Buy"

    def get_prefixes(self):
        return ["buy", "purchase", "b"]

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
                if shop_item.shop_zone_id:
                    profile = get_player_profile(msg.author.id)
                    transaction = attempt_purchase_item(profile, shop_item, purchase_count)
                    save_player_profile(profile)
                    embed = PurchaseResultEmbed(msg.author, transaction)
                    embed_message = await msg.channel.send(embed=embed.generate_embed())
                    await embed.connect_reaction_listener(embed_message)
                else:
                    await msg.channel.send("You cannot purchase this item.")
            else:
                await msg.channel.send("Item not found.")
        except ValueError:
            await msg.channel.send("Enter an item name to use.")
