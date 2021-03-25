#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import convert_dict_keys_to_id, insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.equipment_stat import EquipmentStat
from primerpg.persistence.equipment_stat_categories_persistence import (
    get_all_equipment_stat_categories,
)
from primerpg.persistence.persistence_exception import PersistenceException
from primerpg.persistence.skill_category_persistence import get_all_skill_categories

file_name = "items.json"
equipment_stats_table = "equipment_stats"

select_equipment_stat_query = (
    "SELECT * FROM %s WHERE item_id = ? AND equipment_stat_category_id = ?" % equipment_stats_table
)
select_equipment_stats_query = "SELECT * FROM %s WHERE item_id = ?" % equipment_stats_table
select_all_equipment_stats_query = "SELECT * FROM %s" % equipment_stats_table
create_equipment_stats_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "item_id integer NOT NULL, "
    "equipment_stat_category_id integer NOT NULL, "
    "value integer NOT NULL, "
    "scales_with text NOT NULL, "
    "PRIMARY KEY(item_id, equipment_stat_category_id), "
    "FOREIGN KEY(item_id) REFERENCES items(unique_id), "
    "FOREIGN KEY(equipment_stat_category_id) REFERENCES equipment_stat_categories(unique_id))" % equipment_stats_table
)


def populate_equipment_stats_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, equipment_stats_table):
        return

    eqst_categories = get_all_equipment_stat_categories()
    skill_categories = get_all_skill_categories()
    for item in data["data"]:
        if "stats" not in item:
            continue
        stats = item["stats"]
        for stat in stats:
            stat = convert_dict_keys_to_id(eqst_categories, stat)
            for (
                stat_id,
                value_and_scaling,
            ) in stat.items():
                if not get_equipment_stat(item["unique_id"], stat_id):
                    scalings = convert_dict_keys_to_id(skill_categories, value_and_scaling["scales_with"])
                    equipment_stat = {
                        "item_id": item["unique_id"],
                        "equipment_stat_category_id": stat_id,
                        "value": value_and_scaling["value"],
                        "scales_with": str(scalings),
                    }
                    insert_dictionary(equipment_stats_table, equipment_stat)


def get_equipment_stat(item_id: int, equipment_stat_category_id: int) -> EquipmentStat:
    cursor_obj = connection.cursor()

    stmt_args = (item_id, equipment_stat_category_id)
    statement = select_equipment_stat_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_equipment_stat(result)


def get_equipment_stats(item_id: int) -> list[EquipmentStat]:
    cursor_obj = connection.cursor()

    stmt_args = (item_id,)
    statement = select_equipment_stats_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    return [init_equipment_stat(r) for r in result]


def get_all_equipment_stats() -> list[EquipmentStat]:
    cursor_obj = connection.cursor()

    statement = select_all_equipment_stats_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_equipment_stat(r) for r in result]


def init_equipment_stat(db_row):
    if db_row:
        return EquipmentStat(
            db_row[0],
            db_row[1],
            db_row[2],
            eval(db_row[3]),
        )
    else:
        raise PersistenceException(EquipmentStat)
