#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import (
    convert_list_values_to_id,
    insert_dictionary,
    should_reload_from_file,
)
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.moveset import Moveset
from primerpg.persistence.move_persistence import get_all_moves
from primerpg.persistence.persistence_exception import PersistenceException

file_name = "movesets.json"
movesets_table = "movesets"

select_moveset_query = "SELECT * FROM %s WHERE unique_id = ?" % movesets_table
select_all_movesets_query = "SELECT * FROM %s" % movesets_table
create_movesets_query = (
    "CREATE TABLE IF NOT EXISTS %s (" "unique_id integer PRIMARY KEY, " "move_ids text NOT NULL)" % movesets_table
)


def populate_movesets_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, movesets_table):
        return

    moves = get_all_moves()
    for item in data["data"]:
        if not get_moveset(item["unique_id"]):
            move_ids = convert_list_values_to_id(moves, item["moves"])
            moveset = {
                "unique_id": item["unique_id"],
                "move_ids": str(move_ids),
            }
            insert_dictionary(movesets_table, moveset)


def get_moveset(unique_id: int) -> Moveset:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_moveset_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_moveset(result)


def get_all_movesets() -> list[Moveset]:
    cursor_obj = connection.cursor()

    statement = select_all_movesets_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_moveset(r) for r in result]


def init_moveset(db_row) -> Moveset:
    if db_row:
        return Moveset(
            db_row[0],
            eval(db_row[1]),
        )
    else:
        raise PersistenceException(Moveset)
