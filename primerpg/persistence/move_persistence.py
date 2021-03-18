#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import convert_name_to_id, insert_dictionary
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.damage_type_persistence import get_all_damage_types
from primerpg.persistence.dto.move import Move
from primerpg.persistence.equipment_stat_categories_persistence import (
    get_all_equipment_stat_categories,
)

moves_table = "moves"

select_move_query = "SELECT * FROM %s WHERE unique_id = ?" % moves_table
select_all_moves_query = "SELECT * FROM %s" % moves_table
create_moves_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY, "
    "power integer NOT NULL, "
    "damage_type_id integer NOT NULL, "
    "scaling_equipment_stat_id integer NOT NULL, "
    "success_chance real NOT NULL, "
    "name text NOT NULL, "
    "FOREIGN KEY(damage_type_id) REFERENCES damage_types(unique_id), "
    "FOREIGN KEY(scaling_equipment_stat_id) REFERENCES equipment_stat_categories(unique_id))" % moves_table
)


def populate_moves_table():
    with open(data_folder / "moves.json") as f:
        data = json.load(f)

    damage_types = get_all_damage_types()
    eq_stat_cats = get_all_equipment_stat_categories()
    for item in data:
        if not get_move(item["unique_id"]):
            damage_type_id = convert_name_to_id(damage_types, item["damage_type"])
            scaling_equipment_stat_id = convert_name_to_id(eq_stat_cats, item["scaling_equipment_stat"])
            # TODO Create object and use insert query instead of temporary dict
            move = {
                "name": item["name"],
                "unique_id": item["unique_id"],
                "power": item["power"],
                "damage_type_id": damage_type_id,
                "scaling_equipment_stat_id": scaling_equipment_stat_id,
                "success_chance": item["success_chance"],
            }
            insert_dictionary(moves_table, move)


def get_move(unique_id: int) -> Move:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_move_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_move(result)


def get_all_moves() -> List[Move]:
    cursor_obj = connection.cursor()

    statement = select_all_moves_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_move(r) for r in result]


def init_move(db_row):
    if db_row:
        return Move(
            db_row[0],
            db_row[1],
            db_row[2],
            db_row[3],
            db_row[4],
            db_row[5],
        )
    else:
        return None
