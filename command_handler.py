from commands.add import Add
from commands.collect import Collect
from commands.data import Data
from commands.dice import Dice
from commands.fish import Fish
from commands.hello import Hello
from commands.help import Help
from commands.start import Start
from commands.time import Time
from commands.weather import Weather
from persistence.connection_handler import spam_list

command_registry = []


def load_commands():
    register(Hello())
    register(Help())
    register(Dice())
    register(Add())
    register(Start())
    register(Fish())
    register(Data())
    register(Time())
    register(Collect())
    register(Weather())


def register(command):
    command_registry.append(command)


async def handle_command(msg, split_content):
    print('Command Content: %s' % split_content)
    if len(split_content) < 1:
        return
    if msg.author.id in spam_list:
        await msg.channel.send('Still processing previous command...')
        return
    # TODO Instead of going through all command_registry, only allow some commands based on user's profile
    for command in command_registry:
        if split_content[0].lower().startswith(tuple(command.get_prefixes())):
            await command.run_command(msg, split_content[1:])
            return
    await msg.channel.send('Unknown command, try `.help` to see a list of all commands')
