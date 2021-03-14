import json
from typing import List

from consts import data_folder
from persistence.common_persistence import (
    insert_dictionary,
    convert_dict_keys_to_id,
)
from persistence.connection_handler import connection
from persistence.dto.mob_drop import MobDrop
from persistence.items_persistence import get_all_items

mob_drops_table = "mob_drops"

select_mob_drops_query = (
    "SELECT * FROM %s WHERE mob_id = ? AND item_id = ?" % mob_drops_table
)
select_all_mob_drops_query = "SELECT * FROM %s WHERE mob_id = ?" % mob_drops_table
create_mob_drops_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "mob_id integer NOT NULL, "
    "item_id integer NOT NULL, "
    "drop_rate real NOT NULL, "
    "mean real NOT NULL, "
    "std_dev real NOT NULL, "
    "PRIMARY KEY(mob_id, item_id))" % mob_drops_table
)


def populate_mob_drops_table():
    with open(data_folder / "mobs.json") as f:
        data = json.load(f)

    items = get_all_items()
    for mob in data:
        drops = convert_dict_keys_to_id(items, mob["drops"])
        for drop_item_id, drop_object in drops.items():
            if not get_mob_drop(mob["unique_id"], drop_item_id):
                mob_drop = {
                    "mob_id": mob["unique_id"],
                    "item_id": drop_item_id,
                    "drop_rate": drop_object["drop_rate"],
                    "mean": drop_object["mean"],
                    "std_dev": drop_object["std_dev"],
                }
                insert_dictionary(mob_drops_table, mob_drop)


def get_mob_drop(mob_id: int, skill_id: int) -> MobDrop:
    cursor_obj = connection.cursor()

    stmt_args = (
        mob_id,
        skill_id,
    )
    statement = select_mob_drops_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob_drop(result)


def get_all_mob_drops(mob_id: int) -> List[MobDrop]:
    cursor_obj = connection.cursor()

    stmt_args = (mob_id,)
    statement = select_all_mob_drops_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_mob_drop(x) for x in result]

    return items


def init_mob_drop(db_row):
    if db_row:
        return MobDrop(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4])
    else:
        return None
