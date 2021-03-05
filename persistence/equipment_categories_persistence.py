import json

from consts import data_folder
from data.equipment_category import EquipmentCategory
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection

equipment_categories_table = "equipment_categories"

select_equipment_categories_table = (
    "SELECT * FROM %s WHERE unique_id = ?" % equipment_categories_table
)
create_equipment_categories_table = (
    "CREATE TABLE IF NOT EXISTS %s"
    " (unique_id integer NOT NULL, name text NOT NULL, max_num integer NOT NULL)"
    % equipment_categories_table
)


def populate_equipment_categories_table():
    with open(data_folder / "equipment_categories.json") as f:
        data = json.load(f)

    for item in data:
        if not get_equipment_category(item["unique_id"]):
            insert_dictionary(equipment_categories_table, item)

    connection.commit()


def get_equipment_category(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_equipment_categories_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_equipment_category(result)


def init_equipment_category(db_row):
    if db_row:
        return EquipmentCategory(
            db_row[0],
            db_row[1],
            db_row[2],
        )
    else:
        return None
