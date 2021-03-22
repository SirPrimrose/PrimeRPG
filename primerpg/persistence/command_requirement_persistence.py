#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import (
    insert_dictionary,
    should_reload_from_file,
    convert_list_values_to_id,
    convert_name_to_id,
)
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.command_requirement import CommandRequirement
from primerpg.persistence.player_state_persistence import get_all_player_states
from primerpg.persistence.zone_persistence import get_all_zones

file_name = "command_requirements.json"
command_requirements_table = "command_requirements"

select_command_requirement_query = "SELECT * FROM %s WHERE unique_id = ?" % command_requirements_table
select_all_command_requirements_query = "SELECT * FROM %s" % command_requirements_table
create_command_requirements_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY, "
    "name text NOT NULL, "
    "zone_id integer NOT NULL, "
    "cooldown integer NOT NULL, "
    "allowed_state_ids text NOT NULL, "
    "FOREIGN KEY(zone_id) REFERENCES zones(unique_id))" % command_requirements_table
)


def populate_command_requirements_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, command_requirements_table):
        return

    zones = get_all_zones()
    player_states = get_all_player_states()
    for item in data["data"]:
        if not get_command_requirement(item["unique_id"]):
            zone_id = convert_name_to_id(zones, item["zone"])
            # Handle special case for commands allowed anywhere
            if item["allowed_states"] == "All":
                allowed_state_ids = [state.unique_id for state in player_states]
            else:
                allowed_state_ids = convert_list_values_to_id(player_states, item["allowed_states"])
            command_requirement = {
                "unique_id": item["unique_id"],
                "name": item["name"],
                "zone_id": zone_id,
                "allowed_state_ids": str(allowed_state_ids),
                "cooldown": 0,
            }
            if "cooldown" in item:
                command_requirement["cooldown"] = item["cooldown"]
            insert_dictionary(command_requirements_table, command_requirement)


def get_command_requirement(unique_id: int) -> CommandRequirement:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_command_requirement_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_command_requirement(result)


def get_all_command_requirements() -> List[CommandRequirement]:
    cursor_obj = connection.cursor()

    statement = select_all_command_requirements_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_command_requirement(r) for r in result]


def init_command_requirement(db_row):
    if db_row:
        return CommandRequirement(
            db_row[0],
            db_row[1],
            db_row[2],
            db_row[3],
            eval(db_row[4]),
        )
    else:
        return None
