#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file, convert_name_to_id
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.task_category import TaskCategory
from primerpg.persistence.zone_persistence import get_all_zones

file_name = "task_categories.json"
task_categories_table = "task_categories"

select_task_category_query = "SELECT * FROM %s WHERE unique_id = ?" % task_categories_table
select_task_categories_query = "SELECT * FROM %s WHERE zone_id <= ?" % task_categories_table
select_all_task_categories_query = "SELECT * FROM %s" % task_categories_table
create_task_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY, "
    "zone_id integer NOT NULL, "
    "name text NOT NULL)" % task_categories_table
)


def populate_task_categories_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, task_categories_table):
        return

    zones = get_all_zones()
    for item in data["data"]:
        if not get_task_category(item["unique_id"]):
            task_category = {
                "unique_id": item["unique_id"],
                "zone_id": convert_name_to_id(zones, item["zone"]),
                "name": item["name"],
            }
            insert_dictionary(task_categories_table, task_category)


def get_task_category(unique_id: int) -> TaskCategory:
    """If making a request to get the name or short name, prefer to use the methods provided in data cache.

    :param unique_id: Unique id of the task category
    :return: The task category
    """
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_task_category_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_task_category(result)


def get_task_categories(zone_id: int) -> List[TaskCategory]:
    cursor_obj = connection.cursor()

    stmt_args = (zone_id,)
    statement = select_task_categories_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    return [init_task_category(r) for r in result]


def get_all_task_categories() -> List[TaskCategory]:
    cursor_obj = connection.cursor()

    statement = select_all_task_categories_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_task_category(r) for r in result]


def init_task_category(db_row):
    if db_row:
        return TaskCategory(
            db_row[0],
            db_row[1],
            db_row[2],
        )
    else:
        return None
