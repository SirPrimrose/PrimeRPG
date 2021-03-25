#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import (
    insert_dictionary,
    should_reload_from_file,
    convert_name_to_id,
    convert_list_values_to_id,
)
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.damage_type_persistence import get_all_damage_types
from primerpg.persistence.dto.boss_core import BossCore
from primerpg.persistence.persistence_exception import PersistenceException
from primerpg.persistence.zone_persistence import get_all_zones

file_name = "mobs.json"
bosses_table = "bosses"

select_boss_query = "SELECT * FROM %s WHERE zone_id = ?" % bosses_table
select_bosses_query = "SELECT * FROM %s" % bosses_table
create_bosses_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "mob_id integer PRIMARY KEY,"
    "zone_id integer NOT NULL,"
    "type_strength_ids text NOT NULL,"
    "type_weakness_ids text NOT NULL)" % bosses_table
)


def populate_bosses_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, bosses_table):
        return

    zones = get_all_zones()
    damage_types = get_all_damage_types()
    for item in data["data"]:
        if "boss_data" not in item:
            continue
        if not get_boss(item["unique_id"]):
            boss_data = item["boss_data"]
            boss = {
                "mob_id": item["unique_id"],
                "zone_id": convert_name_to_id(zones, boss_data["zone"]),
                "type_strength_ids": str(convert_list_values_to_id(damage_types, boss_data["type_strengths"])),
                "type_weakness_ids": str(convert_list_values_to_id(damage_types, boss_data["type_weaknesses"])),
            }
            insert_dictionary(bosses_table, boss)


def get_boss(zone_id: int) -> BossCore:
    cursor_obj = connection.cursor()

    stmt_args = (zone_id,)
    statement = select_boss_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_boss(result)


def get_all_bosses() -> list[BossCore]:
    cursor_obj = connection.cursor()

    statement = select_bosses_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_boss(r) for r in result]


def init_boss(db_row) -> BossCore:
    if db_row:
        return BossCore(
            db_row[0],
            db_row[1],
            eval(db_row[2]),
            eval(db_row[3]),
        )
    else:
        raise PersistenceException(BossCore)
