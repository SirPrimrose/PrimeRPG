import json

from consts import data_folder
from data.item_category import ItemCategory
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection, queue_transaction

item_category_table = "item_category"

select_item_category_table = (
    "SELECT * FROM %s WHERE unique_id = ?" % item_category_table
)
create_item_category_table = (
    "CREATE TABLE IF NOT EXISTS %s"
    " (unique_id integer, name text)" % item_category_table
)


def populate_item_category_table():
    with open(data_folder / "item_categories.json") as f:
        data = json.load(f)

    for item in data:
        if not get_item_category_data(item["unique_id"]):
            insert_dictionary(item_category_table, item)

    connection.commit()


def get_item_category_data(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_item_category_table
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
