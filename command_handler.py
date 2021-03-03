from commands.add import Add
from commands.data import Data
from commands.dice import Dice
from commands.fish import Fish
from commands.hello import Hello
from commands.help import Help
from commands.start import Start
from commands.time import Time

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


def register(command):
    command_registry.append(command)


async def handle_command(msg, split_content):
    print('Command Content: %s' % split_content)
    if len(split_content) < 1:
        return
    for command in command_registry:
        if split_content[0].lower().startswith(tuple(command.get_prefixes())):
            await command.run_command(msg, split_content[1:])
            return
    await msg.channel.send('Unknown command, try `.help` to see a list of all commands')
