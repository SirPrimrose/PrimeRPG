import json

from consts import data_folder
from data.item_category import ItemCategory
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection

item_categories_table = "item_categories"

select_item_categories_query = (
    "SELECT * FROM %s WHERE unique_id = ?" % item_categories_table
)
create_item_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL)" % item_categories_table
)


def populate_item_categories_table():
    with open(data_folder / "item_categories.json") as f:
        data = json.load(f)

    for item in data:
        if not get_item_category(item["unique_id"]):
            insert_dictionary(item_categories_table, item)


def get_item_category(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_item_categories_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_item_category(result)


def init_item_category(db_row):
    if db_row:
        return ItemCategory(
            db_row[0],
            db_row[1],
        )
    else:
        return None
