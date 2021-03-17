import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.equipment_stat_category import EquipmentStatCategory

equipment_stat_categories_table = "equipment_stat_categories"

select_equipment_stat_categories_query = "SELECT * FROM %s WHERE unique_id = ?" % equipment_stat_categories_table
select_all_equipment_stat_categories_query = "SELECT * FROM %s" % equipment_stat_categories_table
create_equipment_stat_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL)" % equipment_stat_categories_table
)


def populate_equipment_stat_categories_table():
    with open(data_folder / "equipment_stat_categories.json") as f:
        data = json.load(f)

    for item in data:
        if not get_equipment_stat_category(item["unique_id"]):
            insert_dictionary(equipment_stat_categories_table, item)


def get_equipment_stat_category(unique_id: int) -> EquipmentStatCategory:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_equipment_stat_categories_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_equipment_stat_category(result)


def get_all_equipment_stat_categories() -> List[EquipmentStatCategory]:
    cursor_obj = connection.cursor()

    statement = select_all_equipment_stat_categories_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_equipment_stat_category(r) for r in result]


def init_equipment_stat_category(db_row):
    if db_row:
        return EquipmentStatCategory(
            db_row[0],
            db_row[1],
        )
    else:
        return None
