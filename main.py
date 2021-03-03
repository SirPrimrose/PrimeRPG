import asyncio
import os
import sys
from traceback import print_exc

import discord

import command_handler
import consts
from persistence import persistence

client = discord.Client()
__DEBUG__ = bool(os.getenv('__DEBUG__'))
ready = False


def app_setup():
    persistence.setup_db()
    print('PrimeRPG setup complete')


async def save_to_db():
    await client.wait_until_ready()
    while True:
        persistence.save_queue()
        await asyncio.sleep(1)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'
          .format(client))
    command_handler.load_commands()
    global ready
    ready = True


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if not ready:
        await msg.channel.send('Bot is still loading...')
        return

    if msg.content.startswith('boop'):
        await msg.channel.send('beep')

    if msg.content.startswith('beep'):
        await msg.channel.send('boop')

    try:
        if msg.content.startswith(consts.command_prefix):
            await command_handler.handle_command(msg, msg.content[len(consts.command_prefix):].split())
    except Exception:
        if __DEBUG__:
            print_exc()
            await msg.channel.send('Encountered error: {0}'.format(sys.exc_info()[1]))


app_setup()

# Start bot client
token = os.getenv('BOT_TOKEN')
if not token:
    print(token)
    print(
        'Missing BOT_TOKEN in environment variables. Copy from '
        'https://discord.com/developers/applications/816353796278976512/bot')
client.loop.create_task(save_to_db())
client.run(token)
