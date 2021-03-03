import discord
import os
import command_handler
import consts
import persistence
import sys

client = discord.Client()
__DEBUG__ = bool(os.getenv('__DEBUG__'))


def app_setup():
    persistence.setup_db()
    print('Setup complete')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'
          .format(client))
    command_handler.load_commands()


@client.event
async def on_message(msg):
    if msg.author == client.user:
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
            msg.channel.send('Encountered error: {0}'.format(sys.exc_info()[1]))


app_setup()

# Start bot client
token = os.getenv('BOT_TOKEN')
if not token:
    print(token)
    print(
        'Missing BOT_TOKEN in environment variables. Copy from '
        'https://discord.com/developers/applications/816353796278976512/bot')
client.run(token)
