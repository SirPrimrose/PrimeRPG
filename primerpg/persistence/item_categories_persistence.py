#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.item_category import ItemCategory

file_name = "item_categories.json"
item_categories_table = "item_categories"

select_item_categories_query = "SELECT * FROM %s WHERE unique_id = ?" % item_categories_table
select_all_item_categories_query = "SELECT * FROM %s" % item_categories_table
create_item_categories_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "name text NOT NULL)" % item_categories_table
)


def populate_item_categories_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, item_categories_table):
        return

    for item in data["data"]:
        if not get_item_category(item["unique_id"]):
            insert_dictionary(item_categories_table, item)


def get_item_category(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_item_categories_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_item_category(result)


def get_all_item_categories() -> List[ItemCategory]:
    cursor_obj = connection.cursor()

    statement = select_all_item_categories_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_item_category(r) for r in result]


def init_item_category(db_row):
    if db_row:
        return ItemCategory(
            db_row[0],
            db_row[1],
        )
    else:
        return None
