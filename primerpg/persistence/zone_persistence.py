#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.zone import Zone

file_name = "zones.json"
zones_table = "zones"

select_zones_query = "SELECT * FROM %s WHERE unique_id = ?" % zones_table
select_all_zones_query = "SELECT * FROM %s" % zones_table
create_zones_query = (
    "CREATE TABLE IF NOT EXISTS %s (" "unique_id integer PRIMARY KEY, " "name text NOT NULL)" % zones_table
)


def populate_zones_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, zones_table):
        return

    for item in data["data"]:
        if not get_zone(item["unique_id"]):
            insert_dictionary(zones_table, item)


def get_zone(unique_id: int) -> Zone:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_zones_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_zone(result)


def get_all_zones() -> List[Zone]:
    cursor_obj = connection.cursor()

    statement = select_all_zones_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_zone(r) for r in result]


def init_zone(db_row):
    if db_row:
        return Zone(
            db_row[0],
            db_row[1],
        )
    else:
        return None
