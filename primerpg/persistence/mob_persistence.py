#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.mob_core import MobCore

file_name = "mobs.json"
mobs_table = "mobs"

select_mob_query = "SELECT * FROM %s WHERE unique_id = ?" % mobs_table
select_mobs_query = "SELECT * FROM %s" % mobs_table
create_mobs_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY,"
    "name text NOT NULL,"
    "weight integer NOT NULL,"
    "icon_url text NOT NULL)" % mobs_table
)


def populate_mobs_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, mobs_table):
        return

    for mob in data["data"]:
        if not get_mob(mob["unique_id"]):
            del mob["skills"]
            del mob["equipment"]
            del mob["drops"]
            insert_dictionary(mobs_table, mob)


def get_mob(unique_id: int) -> MobCore:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_mob_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob(result)


def get_all_mobs() -> List[MobCore]:
    cursor_obj = connection.cursor()

    statement = select_mobs_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_mob(r) for r in result]


def init_mob(db_row):
    if db_row:
        return MobCore(
            db_row[0],
            db_row[1],
            db_row[2],
            db_row[3],
        )
    else:
        return None
