#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.player_state import PlayerState

file_name = "player_states.json"
player_states_table = "player_states"

select_player_states_query = "SELECT * FROM %s WHERE unique_id = ?" % player_states_table
select_all_player_states_query = "SELECT * FROM %s" % player_states_table
create_player_states_query = (
    "CREATE TABLE IF NOT EXISTS %s (" "unique_id integer PRIMARY KEY, " "name text NOT NULL)" % player_states_table
)


def populate_player_states_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, player_states_table):
        return

    for item in data["data"]:
        if not get_player_state(item["unique_id"]):
            insert_dictionary(player_states_table, item)


def get_player_state(unique_id: int) -> PlayerState:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_player_states_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_player_state(result)


def get_all_player_states() -> List[PlayerState]:
    cursor_obj = connection.cursor()

    statement = select_all_player_states_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_player_state(r) for r in result]


def init_player_state(db_row):
    if db_row:
        return PlayerState(
            db_row[0],
            db_row[1],
        )
    else:
        return None
