#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.fish import Fish
from primerpg.persistence.persistence_exception import PersistenceException

file_name = "fish.json"
fish_table = "fish"

create_fish_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY, "
    "item_id integer NOT NULL, "
    "name text NOT NULL, "
    "start_time text NOT NULL, "
    "end_time text NOT NULL, "
    "weather text NOT NULL, "
    "weight int NOT NULL) " % fish_table
)
select_id_fish_query = "SELECT * FROM %s WHERE unique_id = ?" % fish_table
select_fish_query = (
    "SELECT * FROM %s WHERE datetime(start_time) <= datetime(?) AND datetime(end_time) >= datetime("
    "?) AND weather = 'both' OR weather = ?" % fish_table
)


def populate_fish_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, fish_table):
        return

    for fish in data["data"]:
        if not get_fish_from_id(fish["unique_id"]):
            insert_dictionary(fish_table, fish)


def get_fish_from_id(unique_id: int) -> Fish:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_id_fish_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_fish(result)


def get_fish(time: str, weather: str) -> list[Fish]:
    cursor_obj = connection.cursor()

    stmt_args = (time, time, weather)
    statement = select_fish_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    return [init_fish(x) for x in result]


def init_fish(db_row) -> Fish:
    if db_row:
        return Fish(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5], db_row[6])
    else:
        raise PersistenceException(Fish)
