from typing import List

import discord

import persistence
from commands.command import Command
from player import idle_state, gathering_state


class Fish(Command):
    def get_description(self):
        return 'Fish some fish.'

    def get_name(self):
        return 'Fish'

    def get_prefixes(self):
        return ['fish', 'fishing', 'fsh']

    async def run_command(self, msg: discord.Message, args: List[str]):
        player_id = msg.author.id
        player_data = persistence.get_player_data(player_id)
        if player_data.state == idle_state:
            player_data.state = gathering_state
            persistence.update_player_data(player_data.unique_id, vars(player_data))
            # create gather task
            await msg.channel.send('Started fishing.')
        else:
            await msg.channel.send('You are busy {0}.'.format(player_data.state))
