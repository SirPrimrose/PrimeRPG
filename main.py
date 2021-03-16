import asyncio
import os
import sys
from traceback import print_exc

import command_handler
from consts import game_client, command_prefix
from data_cache import load_util_data
from helpers.regen_helper import regen_tick
from logging_handler import setup_logging
from persistence import persistence

# System Env Vars
__DEBUG__ = bool(os.getenv("__DEBUG__"))

# Main File Vars
ready = False
game_tick_rate = 0.5  # seconds
save_tick_rate = 1  # ticks
regen_tick_rate = 120  # ticks

# Quick Config Options
start_app = True  # Start the bot application and connect to Discord. Disable to test without a connection.


def app_setup():
    setup_logging()
    persistence.setup_db()
    load_util_data()
    print("PrimeRPG setup complete")


async def game_tick():
    await game_client.wait_until_ready()
    tick = 0
    while True:
        await asyncio.sleep(game_tick_rate)
        tick += 1
        try:
            if tick % save_tick_rate == 0:
                persistence.save_queue()
            if tick % regen_tick_rate == 0:
                regen_tick()
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
async def on_message(msg):
    if msg.author == game_client.user:
        return

    try:
        if msg.content.startswith(command_prefix):
            if not ready:
                await msg.channel.send("Bot is still loading...")
                return
            await command_handler.handle_command(
                msg, msg.content[len(command_prefix) :].split()
            )
    except Exception:
        print_exc()
        await msg.channel.send("Encountered error: {0}".format(sys.exc_info()[1]))


app_setup()

# Start bot client
if start_app:
    token = os.getenv("BOT_TOKEN")
    if not token:
        print(token)
        print(
            "Missing BOT_TOKEN in environment variables. Copy from "
            "https://discord.com/developers/applications/816353796278976512/bot"
        )
    else:
        game_client.loop.create_task(game_tick())
        game_client.run(token)
else:
    print("Running in non-connected mode. Will not login to Discord.")
