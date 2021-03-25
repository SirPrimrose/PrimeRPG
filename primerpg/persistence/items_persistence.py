#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file, convert_name_to_id
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.item import Item
from primerpg.persistence.zone_persistence import get_all_zones

file_name = "items.json"
items_table = "items"

select_items_query = "SELECT * FROM %s WHERE unique_id = ?" % items_table
select_shop_items_query = "SELECT * FROM %s WHERE shop_zone_id = ? ORDER BY item_category_id, unique_id" % items_table
select_all_items_query = "SELECT * FROM %s" % items_table
create_items_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY, "
    "item_category_id integer NOT NULL, "
    "equipment_category_id integer NOT NULL, "
    "name text NOT NULL, "
    "value integer NOT NULL, "
    "shop_zone_id integer, "
    "moveset_ids text NOT NULL, "
    "usage_effects text NOT NULL)" % items_table
)


def populate_items_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, items_table):
        return

    zones = get_all_zones()
    for item in data["data"]:
        if not get_item(item["unique_id"]):
            item_row = {
                "unique_id": item["unique_id"],
                "item_category_id": item["item_category_id"],
                "equipment_category_id": item["equipment_category_id"],
                "name": item["name"],
                "value": item["value"],
                "shop_zone_id": None,
                "moveset_ids": "[]",
                "usage_effects": "[]",
            }
            if "shop_zone" in item:
                item_row["shop_zone_id"] = convert_name_to_id(zones, item["shop_zone"])
            if "moveset_ids" in item:
                item_row["moveset_ids"] = str(item["moveset_ids"])
            if "usage_effects" in item:
                item_row["usage_effects"] = str(item["usage_effects"])
            insert_dictionary(items_table, item_row)


def get_item(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_items_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_item(result)


def get_shop_items(zone_id: int) -> List[Item]:
    cursor_obj = connection.cursor()

    stmt_args = (zone_id,)
    statement = select_shop_items_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    return [init_item(r) for r in result]


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
            db_row[5],
            eval(db_row[6]),
            eval(db_row[7]),
        )
    else:
        return None
