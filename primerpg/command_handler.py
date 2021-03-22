#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from primerpg.commands.cm_buy import Buy
from primerpg.commands.cm_collect import Collect
from primerpg.commands.cm_equip import Equip
from primerpg.commands.cm_equipment import Equipment
from primerpg.commands.cm_heal import Heal
from primerpg.commands.cm_help import Help
from primerpg.commands.cm_inventory import Inventory
from primerpg.commands.cm_profile import Profile
from primerpg.commands.cm_recon import Recon
from primerpg.commands.cm_scrub import Scrub
from primerpg.commands.cm_shop import Shop
from primerpg.commands.cm_skills import Skills
from primerpg.commands.cm_start import Start
from primerpg.commands.cm_tasks import Tasks
from primerpg.commands.cm_unequip import Unequip
from primerpg.commands.cm_use import Use
from primerpg.commands.cm_world import World
from primerpg.commands.command import Command
from primerpg.data_cache import get_command_requirement_by_name, get_player_state_name
from primerpg.persistence.connection_handler import spam_list
from primerpg.persistence.player_persistence import get_player

command_registry: List[Command] = []


def load_commands():
    register(Help())
    register(Start())
    register(Tasks())
    register(World())
    register(Recon())
    register(Skills())
    register(Heal())
    register(Profile())
    register(Inventory())
    register(Scrub())
    register(Equip())
    register(Unequip())
    register(Equipment())
    register(Collect())
    register(Shop())
    register(Buy())
    register(Use())


def register(command):
    command_registry.append(command)


async def handle_command(msg, split_content: List[str]):
    if len(split_content) < 1:
        return
    if msg.author.id in spam_list:
        await msg.channel.send("Still processing previous command...")
        return
    for command in command_registry:
        if split_content[0].lower() in tuple(command.get_prefixes()):
            can_execute, err_msg = verify_command_usage(msg.author.id, command)
            if can_execute:
                await command.run_command(msg, split_content[1:])
                return
            else:
                await msg.channel.send(err_msg)
                return
    await msg.channel.send("Unknown command, try `.help` to see a list of all commands")


def verify_command_usage(player_id: int, command: Command) -> (bool, str):
    command_req = get_command_requirement_by_name(command.get_name())
    if command_req:
        player_core = get_player(player_id)
        if not player_core:
            if command_req.zone_id == 0:
                return True, ""
            else:
                return False, "Please create your account first using `.start`"
        else:
            if player_core.zone_id >= command_req.zone_id:
                if player_core.state_id in command_req.allowed_state_ids:
                    return True, ""
                else:
                    # Player is not in a correct state
                    return False, "Cannot perform command in current state: {}".format(
                        get_player_state_name(player_core.state_id)
                    )
            else:
                # Player is not at a high enough zone
                return False, "Unlock this command in zone {}. Try .help to see available commands.".format(
                    command_req.zone_id
                )
    else:
        # Command requirement doesn't exist for some reason, allow usage
        print('Command "{}" does not have requirement!'.format(command.get_name()))
        return True, ""
