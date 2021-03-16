import json
from typing import List

from consts import data_folder
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection
from persistence.dto.task_category import TaskCategory

task_categories_table = "task_categories"

select_task_categories_query = (
    "SELECT * FROM %s WHERE unique_id = ?" % task_categories_table
)
select_all_task_categories_query = "SELECT * FROM %s" % task_categories_table
create_task_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL)" % task_categories_table
)


def populate_task_categories_table():
    with open(data_folder / "task_categories.json") as f:
        data = json.load(f)

    for item in data:
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
