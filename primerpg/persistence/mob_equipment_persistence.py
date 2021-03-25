#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.data.entity_equipment import EntityEquipment
from primerpg.persistence.common_persistence import convert_dict_keys_to_id, insert_dictionary, should_reload_from_file
from primerpg.persistence.connection_handler import connection, queue_transaction
from primerpg.persistence.equipment_categories_persistence import get_all_equipment_categories
from primerpg.persistence.items_persistence import get_all_items
from primerpg.persistence.persistence_exception import PersistenceException

file_name = "mobs.json"
mob_equipment_table = "mob_equipment"

select_mob_equipment_query = "SELECT * FROM %s WHERE mob_id = ? AND equipment_category_id = ?" % mob_equipment_table
select_all_mob_equipment_query = "SELECT * FROM %s WHERE mob_id = ?" % mob_equipment_table
create_mob_equipment_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "mob_id integer NOT NULL, "
    "equipment_category_id integer NOT NULL, "
    "item_id integer NOT NULL)" % mob_equipment_table
)
update_mob_equipment_query = (
    "UPDATE %s SET item_id = ? WHERE mob_id = ? AND equipment_category_id = ?" % mob_equipment_table
)
insert_mob_equipment_query = (
    "INSERT INTO %s (mob_id, equipment_category_id, item_id) VALUES (?, ?, ?)" % mob_equipment_table
)
delete_mob_equipment_query = "DELETE from %s WHERE mob_id = ?" % mob_equipment_table


def populate_mob_equipment_table():
    with open(data_folder / file_name) as f:
        data = json.load(f)

    if not should_reload_from_file(data["dependencies"], file_name, mob_equipment_table):
        return

    equipment_categories = get_all_equipment_categories()
    items = get_all_items()
    for mob in data["data"]:
        equipment = convert_dict_keys_to_id(equipment_categories, mob["equipment"])
        equipment = convert_dict_keys_to_id(items, equipment, True)
        for equipment_category_id, item_id in equipment.items():
            if not get_mob_equipment(mob["unique_id"], equipment_category_id):
                mob_equipment = {
                    "mob_id": mob["unique_id"],
                    "equipment_category_id": equipment_category_id,
                    "item_id": item_id,
                }
                insert_dictionary(mob_equipment_table, mob_equipment)


def get_mob_equipment(mob_id: int, equipment_category_id: int) -> EntityEquipment:
    cursor_obj = connection.cursor()

    stmt_args = (
        mob_id,
        equipment_category_id,
    )
    statement = select_mob_equipment_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob_equipment(result)


def get_all_mob_equipment(mob_id: int) -> list[EntityEquipment]:
    cursor_obj = connection.cursor()

    stmt_args = (mob_id,)
    statement = select_all_mob_equipment_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_mob_equipment(x) for x in result]

    return items


def insert_mob_equipment(equipment: EntityEquipment):
    stmt = insert_mob_equipment_query
    stmt_args = (
        equipment.entity_id,
        equipment.equipment_category_id,
        equipment.item_id,
    )
    queue_transaction(equipment.entity_id, stmt, stmt_args)


def update_mob_equipment(equipment: EntityEquipment):
    stmt = update_mob_equipment_query
    stmt_args = (
        equipment.item_id,
        equipment.entity_id,
        equipment.equipment_category_id,
    )
    queue_transaction(equipment.entity_id, stmt, stmt_args)


def delete_mob_equipment(mob_id: int):
    stmt = delete_mob_equipment_query
    stmt_args = (mob_id,)
    queue_transaction(mob_id, stmt, stmt_args)


def init_mob_equipment(db_row) -> EntityEquipment:
    if db_row:
        return EntityEquipment(db_row[0], db_row[1], db_row[2])
    else:
        raise PersistenceException(EntityEquipment)
