from typing import List

import discord

import persistence
from commands.command import Command


class Start(Command):
    def get_description(self):
        return 'Start the game.'

    def get_name(self):
        return 'Start'

    def get_prefixes(self):
        return ['start', 'signup', 'begin']

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_data = persistence.get_player_data(player_id)
        if player_data:
            await msg.channel.send('You are already playing {0}.'.format(msg.author.name))
        else:
            persistence.create_player_data(player_id, msg.author.name)
            await msg.channel.send('Welcome to the game {0}'.format(msg.author.name))
