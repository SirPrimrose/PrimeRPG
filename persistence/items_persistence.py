import json

from consts import data_folder
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection, queue_transaction

items_table = "items"

select_items_table = "SELECT * FROM %s WHERE unique_id = ?" % items_table
create_items_table = (
    "CREATE TABLE IF NOT EXISTS %s"
    " (unique_id integer, name text, value integer)" % items_table
)
insert_items_table = (
    "INSERT INTO %s (unique_id, name, value) VALUES (?, ?, ?)" % items_table
)
delete_items_table = "DELETE from %s WHERE unique_id = ?" % items_table


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

    return result


def insert_item_data(unique_id: int, name: str, value: int):
    stmt = insert_items_table
    stmt_args = (unique_id, name, value)
    queue_transaction(unique_id, stmt, stmt_args)


def delete_item_data(unique_id: int):
    stmt = delete_items_table
    stmt_args = (unique_id,)
    queue_transaction(unique_id, stmt, stmt_args)
