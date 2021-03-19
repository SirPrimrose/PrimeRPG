#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from primerpg.commands.cm_add import Add
from primerpg.commands.cm_collect import World
from primerpg.commands.cm_data import Data
from primerpg.commands.cm_dice import Dice
from primerpg.commands.cm_embed import EmbedCommand
from primerpg.commands.cm_equip import Equip
from primerpg.commands.cm_equipment import Equipment
from primerpg.commands.cm_heal import Heal
from primerpg.commands.cm_hello import Hello
from primerpg.commands.cm_help import Help
from primerpg.commands.cm_inventory import Inventory
from primerpg.commands.cm_profile import Profile
from primerpg.commands.cm_recon import Recon
from primerpg.commands.cm_scrub import Scrub
from primerpg.commands.cm_skills import Skills
from primerpg.commands.cm_start import Start
from primerpg.commands.cm_tasks import Tasks
from primerpg.commands.cm_unequip import Unequip
from primerpg.persistence.connection_handler import spam_list

command_registry = []


def load_commands():
    register(Hello())
    register(Help())
    register(Dice())
    register(Add())
    register(Start())
    register(Tasks())
    register(Data())
    register(World())
    register(Recon())
    register(EmbedCommand())
    register(Skills())
    register(Heal())
    register(Profile())
    register(Inventory())
    register(Scrub())
    register(Equip())
    register(Unequip())
    register(Equipment())


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
