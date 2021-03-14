import json
from typing import List

from consts import data_folder
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection
from persistence.dto.equipment_category import EquipmentCategory

equipment_categories_table = "equipment_categories"

select_equipment_categories_query = (
    "SELECT * FROM %s WHERE unique_id = ?" % equipment_categories_table
)
select_all_equipment_categories_query = "SELECT * FROM %s" % equipment_categories_table
create_equipment_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL, "
    "max_num integer NOT NULL)" % equipment_categories_table
)


def populate_equipment_categories_table():
    with open(data_folder / "equipment_categories.json") as f:
        data = json.load(f)

    for item in data:
        if not get_equipment_category(item["unique_id"]):
            insert_dictionary(equipment_categories_table, item)


def get_equipment_category(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_equipment_categories_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_equipment_category(result)


def get_all_equipment_categories() -> List[EquipmentCategory]:
    cursor_obj = connection.cursor()

    statement = select_all_equipment_categories_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_equipment_category(r) for r in result]


def init_equipment_category(db_row):
    if db_row:
        return EquipmentCategory(
            db_row[0],
            db_row[1],
            db_row[2],
        )
    else:
        return None
