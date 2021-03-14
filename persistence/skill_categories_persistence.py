import json
from typing import List

from consts import data_folder
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection
from persistence.dto.skill_category import SkillCategory

skill_categories_table = "skill_categories"

select_skill_categories_query = (
    "SELECT * FROM %s WHERE unique_id = ?" % skill_categories_table
)
select_all_skill_categories_query = "SELECT * FROM %s" % skill_categories_table
create_skill_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL, "
    "short_name text NOT NULL)" % skill_categories_table
)


def populate_skill_categories_table():
    with open(data_folder / "skill_categories.json") as f:
        data = json.load(f)

    for item in data:
        if not get_skill_category(item["unique_id"]):
            insert_dictionary(skill_categories_table, item)


def get_skill_category(unique_id: int) -> SkillCategory:
    """If making a request to get the name or short name, prefer to use the methods provided in util.

    :param unique_id: Unique id of the skill category
    :return: The skill category
    """
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_skill_categories_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_skill_category(result)


def get_all_skill_categories() -> List[SkillCategory]:
    cursor_obj = connection.cursor()

    statement = select_all_skill_categories_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_skill_category(r) for r in result]


def init_skill_category(db_row):
    if db_row:
        return SkillCategory(
            db_row[0],
            db_row[1],
            db_row[2],
        )
    else:
        return None
