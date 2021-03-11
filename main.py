import asyncio
import os
import sys
import time
from traceback import print_exc

import command_handler
from consts import game_client, command_prefix
from persistence import persistence

# System Env Vars
__DEBUG__ = bool(os.getenv("__DEBUG__"))

# Main File Vars
from persistence.skill_categories_persistence import get_skill_category
from util import load_util_data, get_skill_category_name

ready = False

# Quick Config Options
start_app = True  # Start the bot application and connect to Discord. Disable to test without a connection.


def app_setup():
    persistence.setup_db()
    load_util_data()
    print("PrimeRPG setup complete")


async def save_to_db():
    await game_client.wait_until_ready()
    while True:
        persistence.save_queue()
        await asyncio.sleep(1)


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
        if __DEBUG__:
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
        game_client.loop.create_task(save_to_db())
        game_client.run(token)
else:
    print("Running in non-connected mode. Will not login to Discord.")
