import json
from typing import List

from consts import data_folder
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection
from persistence.dto.damage_type import DamageType

damage_types_table = "damage_types"

select_damage_types_query = "SELECT * FROM %s WHERE unique_id = ?" % damage_types_table
select_all_damage_types_query = "SELECT * FROM %s" % damage_types_table
create_damage_types_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL)" % damage_types_table
)


def populate_damage_types_table():
    with open(data_folder / "damage_types.json") as f:
        data = json.load(f)

    for item in data:
        if not get_damage_type(item["unique_id"]):
            insert_dictionary(damage_types_table, item)


def get_damage_type(unique_id: int) -> DamageType:
    """If making a request to get the name or short name, prefer to use the methods provided in util.

    :param unique_id: Unique id of the skill category
    :return: The skill category
    """
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_damage_types_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_skill_category(result)


def get_all_damage_types() -> List[DamageType]:
    cursor_obj = connection.cursor()

    statement = select_all_damage_types_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_skill_category(r) for r in result]


def init_skill_category(db_row):
    if db_row:
        return DamageType(
            db_row[0],
            db_row[1],
        )
    else:
        return None
