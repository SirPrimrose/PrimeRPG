#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.task_category import TaskCategory

file_name = "task_categories.json"
task_categories_table = "task_categories"

select_task_categories_query = "SELECT * FROM %s WHERE unique_id = ?" % task_categories_table
select_all_task_categories_query = "SELECT * FROM %s" % task_categories_table
create_task_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL)" % task_categories_table
)


def populate_task_categories_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, task_categories_table):
        return

    for item in data["data"]:
        if not get_skill_category(item["unique_id"]):
            insert_dictionary(task_categories_table, item)


def get_skill_category(unique_id: int) -> TaskCategory:
    """If making a request to get the name or short name, prefer to use the methods provided in util.

    :param unique_id: Unique id of the skill category
    :return: The skill category
    """
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_task_categories_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_skill_category(result)


def get_all_task_categories() -> List[TaskCategory]:
    cursor_obj = connection.cursor()

    statement = select_all_task_categories_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_skill_category(r) for r in result]


def init_skill_category(db_row):
    if db_row:
        return TaskCategory(
            db_row[0],
            db_row[1],
        )
    else:
        return None
