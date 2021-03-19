#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.persistence.common_persistence import insert_dictionary, should_reload_from_file, convert_name_to_id
from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.shop_item import ShopItem
from primerpg.persistence.zone_persistence import get_all_zones

file_name = "items.json"
shop_items_table = "shop_items"

select_shop_item_query = "SELECT * FROM %s WHERE item_id = ?" % shop_items_table
select_all_shop_items_query = "SELECT * FROM %s" % shop_items_table
create_shop_items_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "item_id integer PRIMARY KEY, "
    "cost integer NOT NULL, "
    "zone_id integer NOT NULL, "
    "FOREIGN KEY(item_id) REFERENCES items(unique_id))" % shop_items_table
)


def populate_shop_items_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, shop_items_table):
        return

    zones = get_all_zones()
    for item in data["data"]:
        if "shop_item" not in item:
            continue
        if not get_shop_item(item["unique_id"]):
            shop_item_entry = item["shop_item"]
            zone_id = convert_name_to_id(zones, shop_item_entry["zone"])
            shop_item = {"item_id": item["unique_id"], "cost": shop_item_entry["cost"], "zone_id": zone_id}
            insert_dictionary(shop_items_table, shop_item)


def get_shop_item(item_id: int) -> ShopItem:
    cursor_obj = connection.cursor()

    stmt_args = (item_id,)
    statement = select_shop_item_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_shop_item(result)


def get_all_shop_items() -> List[ShopItem]:
    cursor_obj = connection.cursor()

    statement = select_all_shop_items_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_shop_item(r) for r in result]


def init_shop_item(db_row):
    if db_row:
        return ShopItem(
            db_row[0],
            db_row[1],
            db_row[2],
        )
    else:
        return None
