import discord
import os

client = discord.Client()
commandPrefix = '.'
commandHello = 'hello'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'
          .format(client))


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('boop'):
        await msg.channel.send('beep')

    if msg.content.startswith('beep'):
        await msg.channel.send('boop')

    if msg.content.startswith(commandPrefix):
        await handle_command(msg, msg.content[len(commandPrefix):])


async def handle_command(msg, suffix):
    print(suffix)
    if suffix.startswith(commandHello):
        await handle_hello(msg)


async def handle_hello(msg):
    if msg.author.nick:
        await msg.channel.send('Hello {0.author.name}, or should I call you {0.author.nick}?'
                               .format(msg))
    else:
        await msg.channel.send('Hello {0.author.name}... it seems that\'s all you go by.'
                               .format(msg))


token = os.getenv('BOT_TOKEN')
if not token:
    print(token)
    print(
        'Missing BOT_TOKEN in environment variables. Copy from '
        'https://discord.com/developers/applications/816353796278976512/bot')
client.run(token)
