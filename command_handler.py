from typing import List

from commands.cm_add import Add
from commands.cm_collect import Collect
from commands.cm_data import Data
from commands.cm_dice import Dice
from commands.cm_embed import EmbedCommand
from commands.cm_fish import Fish
from commands.cm_heal import Heal
from commands.cm_hello import Hello
from commands.cm_help import Help
from commands.cm_inventory import Inventory
from commands.cm_profile import Profile
from commands.cm_recon import Recon
from commands.cm_scrub import Scrub
from commands.cm_skills import Skills
from commands.cm_start import Start
from commands.cm_time import Time
from commands.cm_weather import Weather
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
    register(Recon())
    register(EmbedCommand())
    register(Skills())
    register(Heal())
    register(Profile())
    register(Inventory())
    register(Scrub())


def register(command):
    command_registry.append(command)


async def handle_command(msg, split_content: List[str]):
    print("Command Content: %s" % split_content)
    if len(split_content) < 1:
        return
    if msg.author.id in spam_list:
        await msg.channel.send("Still processing previous command...")
        return
    # TODO Instead of going through all command_registry, only allow some commands based on user's profile
    for command in command_registry:
        if split_content[0].lower() in tuple(command.get_prefixes()):
            await command.run_command(msg, split_content[1:])
            return
    await msg.channel.send("Unknown command, try `.help` to see a list of all commands")
