import json
from typing import List

from consts import data_folder
from data.item import Item
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection

items_table = "items"

select_items_query = "SELECT * FROM %s WHERE unique_id = ?" % items_table
select_all_items_query = "SELECT * FROM %s" % items_table
create_items_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "item_category_id integer NOT NULL, "
    "equipment_category_id integer NOT NULL, "
    "name text NOT NULL, "
    "value integer NOT NULL)" % items_table
)


def populate_items_table():
    with open(data_folder / "items.json") as f:
        data = json.load(f)

    for item in data:
        if not get_item(item["unique_id"]):
            insert_dictionary(items_table, item)


def get_item(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_items_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_item(result)


def get_all_items() -> List[Item]:
    cursor_obj = connection.cursor()

    statement = select_all_items_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_item(r) for r in result]


def init_item(db_row):
    if db_row:
        return Item(
            db_row[0],
            db_row[1],
            db_row[2],
            db_row[3],
            db_row[4],
        )
    else:
        return None
