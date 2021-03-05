import json

from consts import data_folder
from data.skill_category import SkillCategory
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection

skill_categories_table = "skill_categories"

select_skill_categories_table = (
    "SELECT * FROM %s WHERE unique_id = ?" % skill_categories_table
)
create_skill_categories_table = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL)" % skill_categories_table
)


def populate_skill_categories_table():
    with open(data_folder / "skill_categories.json") as f:
        data = json.load(f)

    for item in data:
        if not get_skill_category(item["unique_id"]):
            insert_dictionary(skill_categories_table, item)


def get_skill_category(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_skill_categories_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_skill_category(result)


def init_skill_category(db_row):
    if db_row:
        return SkillCategory(
            db_row[0],
            db_row[1],
        )
    else:
        return None
