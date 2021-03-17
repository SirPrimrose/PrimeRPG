import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.item_moveset import ItemMoveset

item_movesets_table = "item_movesets"

select_item_moveset_query = "SELECT * FROM %s WHERE item_id = ?" % item_movesets_table
select_all_item_movesets_query = "SELECT * FROM %s" % item_movesets_table
create_item_movesets_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "item_id integer PRIMARY KEY, "
    "moveset_ids text NOT NULL, "
    "FOREIGN KEY(item_id) REFERENCES items(unique_id))" % item_movesets_table
)


def populate_item_movesets_table():
    with open(data_folder / "items.json") as f:
        data = json.load(f)

    for item in data:
        if not get_item_moveset(item["unique_id"]) and "moveset_ids" in item:
            item_moveset = {
                "item_id": item["unique_id"],
                "moveset_ids": str(item["moveset_ids"]),
            }
            insert_dictionary(item_movesets_table, item_moveset)


def get_item_moveset(item_id: int) -> ItemMoveset:
    cursor_obj = connection.cursor()

    stmt_args = (item_id,)
    statement = select_item_moveset_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_item_moveset(result)


def get_all_item_movesets() -> List[ItemMoveset]:
    cursor_obj = connection.cursor()

    statement = select_all_item_movesets_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_item_moveset(r) for r in result]


def init_item_moveset(db_row):
    if db_row:
        return ItemMoveset(
            db_row[0],
            eval(db_row[1]),
        )
    else:
        return None
