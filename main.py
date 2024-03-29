#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import asyncio
import os
import sys
from traceback import print_exc

from discord import Message

from primerpg import command_handler
from primerpg.consts import game_client, command_prefix
from primerpg.data_cache import load_util_data
from primerpg.helpers.regen_helper import regen_tick
from primerpg.logging_handler import setup_logging
from primerpg.persistence import persistence_main
from primerpg.persistence.player_rank_persistence import generate_player_ranks
from settings import env_setup, get_env_var

# System Env Vars
__DEBUG__ = bool(os.getenv("__DEBUG__"))

# Main File Vars
ready = False
game_tick_rate = 0.5  # seconds
save_tick_rate = 1  # ticks
regen_tick_rate = 120  # ticks
rank_tick_rate = 900  # ticks

# Quick Config Options
start_app = True  # Start the bot application and connect to Discord. Disable to test without a connection.


def app_setup():
    setup_logging()
    persistence_main.setup_db()
    load_util_data()
    env_setup()
    print("PrimeRPG setup complete")


async def game_tick():
    await game_client.wait_until_ready()
    tick = 0
    while True:
        await asyncio.sleep(game_tick_rate)
        tick += 1
        try:
            if tick % save_tick_rate == 0:
                persistence_main.save_queue()
            if tick % regen_tick_rate == 0:
                regen_tick()
            if tick % rank_tick_rate == 0:
                generate_player_ranks()
        except Exception:
            print_exc()
            print("Encountered error: {0}".format(sys.exc_info()[1]))


@game_client.event
async def on_ready():
    print("We have logged in as {0.user}".format(game_client))
    command_handler.load_commands()
    global ready
    ready = True


@game_client.event
async def on_message(msg: Message):
    if msg.author == game_client.user:
        return

    try:
        if msg.content.startswith(command_prefix):
            if not ready:
                await msg.channel.send("Bot is still loading...")
                return
            await command_handler.handle_command(msg, msg.content[len(command_prefix) :].split())
    except Exception:
        print_exc()
        await msg.channel.send("Encountered error: {0}".format(sys.exc_info()[1]))


app_setup()

# Start bot client
if start_app:
    bot_token = get_env_var("BOT_TOKEN")
    if not bot_token:
        print(
            "Missing BOT_TOKEN in environment variables. Copy from "
            "https://discord.com/developers/applications/816353796278976512/bot"
        )
    else:
        game_client.loop.create_task(game_tick())
        game_client.run(bot_token)
else:
    print("Running in non-connected mode. Will not login to Discord.")
