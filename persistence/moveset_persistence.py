import json
from typing import List

from consts import data_folder
from persistence.common_persistence import (
    insert_dictionary,
    convert_list_values_to_id,
)
from persistence.connection_handler import connection
from persistence.dto.moveset import Moveset
from persistence.move_persistence import get_all_moves

movesets_table = "movesets"

select_moveset_query = "SELECT * FROM %s WHERE unique_id = ?" % movesets_table
select_all_movesets_query = "SELECT * FROM %s" % movesets_table
create_movesets_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY, "
    "move_ids text NOT NULL)" % movesets_table
)


def populate_movesets_table():
    with open(data_folder / "movesets.json") as f:
        data = json.load(f)

    moves = get_all_moves()
    for item in data:
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


def get_all_movesets() -> List[Moveset]:
    cursor_obj = connection.cursor()

    statement = select_all_movesets_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_moveset(r) for r in result]


def init_moveset(db_row):
    if db_row:
        return Moveset(
            db_row[0],
            db_row[1],
        )
    else:
        return None
