import json

from consts import data_folder
from data.item import Item
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection, queue_transaction

items_table = "items"

select_items_table = "SELECT * FROM %s WHERE unique_id = ?" % items_table
create_items_table = (
    "CREATE TABLE IF NOT EXISTS %s"
    " (unique_id integer NOT NULL, category_id integer NOT NULL,name text NOT NULL, value integer NOT NULL)"
    % items_table
)


def populate_item_table():
    with open(data_folder / "items.json") as f:
        data = json.load(f)

    for item in data:
        if not get_item_data(item["unique_id"]):
            insert_dictionary(items_table, item)

    connection.commit()


def get_item_data(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_items_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_item(result)


def init_item(db_row):
    if db_row:
        return Item(
            db_row[0],
            db_row[1],
            db_row[2],
            db_row[3],
        )
    else:
        return None
