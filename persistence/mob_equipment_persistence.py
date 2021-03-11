import json
from typing import List

from consts import data_folder
from data.mob_equipment import MobEquipment
from persistence.common_persistence import (
    insert_dictionary,
    convert_dict_keys_to_id,
)
from persistence.connection_handler import connection, queue_transaction
from persistence.equipment_categories_persistence import get_all_equipment_categories
from persistence.items_persistence import get_all_items

mob_equipment_table = "mob_equipment"

select_mob_equipment_query = (
    "SELECT * FROM %s WHERE mob_id = ? AND equipment_slot_id = ?" % mob_equipment_table
)
select_all_mob_equipment_query = (
    "SELECT * FROM %s WHERE mob_id = ?" % mob_equipment_table
)
create_mob_equipment_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "mob_id integer NOT NULL, "
    "equipment_slot_id integer NOT NULL, "
    "item_id integer NOT NULL)" % mob_equipment_table
)
update_mob_equipment_query = (
    "UPDATE %s SET item_id = ? WHERE mob_id = ? AND equipment_slot_id = ?"
    % mob_equipment_table
)
insert_mob_equipment_query = (
    "INSERT INTO %s (mob_id, equipment_slot_id, item_id) VALUES (?, ?, ?)"
    % mob_equipment_table
)
delete_mob_equipment_query = "DELETE from %s WHERE mob_id = ?"


def populate_mob_equipment_table():
    with open(data_folder / "mobs.json") as f:
        data = json.load(f)

    equipment_categories = get_all_equipment_categories()
    items = get_all_items()
    for mob in data:
        equipment = convert_dict_keys_to_id(equipment_categories, mob["equipment"])
        equipment = convert_dict_keys_to_id(items, equipment, True)
        for equipment_slot_id, item_id in equipment.items():
            if not get_mob_equipment(mob["unique_id"], equipment_slot_id):
                mob_equipment = {
                    "mob_id": mob["unique_id"],
                    "equipment_slot_id": equipment_slot_id,
                    "item_id": item_id,
                }
                insert_dictionary(mob_equipment_table, mob_equipment)


def get_mob_equipment(mob_id: int, equipment_slot_id: int) -> MobEquipment:
    cursor_obj = connection.cursor()

    stmt_args = (
        mob_id,
        equipment_slot_id,
    )
    statement = select_mob_equipment_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob_equipment(result)


def get_all_mob_equipment(mob_id: int) -> List[MobEquipment]:
    cursor_obj = connection.cursor()

    stmt_args = (mob_id,)
    statement = select_all_mob_equipment_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_mob_equipment(x) for x in result]

    return items


def insert_mob_equipment(equipment: MobEquipment):
    stmt = insert_mob_equipment_query
    stmt_args = (equipment.get_mob_id(), equipment.equipment_slot_id, equipment.item_id)
    queue_transaction(equipment.get_mob_id(), stmt, stmt_args)


def update_mob_equipment(equipment: MobEquipment):
    stmt = update_mob_equipment_query
    stmt_args = (equipment.item_id, equipment.get_mob_id(), equipment.equipment_slot_id)
    queue_transaction(equipment.get_mob_id(), stmt, stmt_args)


def delete_mob_equipment(mob_id: int):
    stmt = delete_mob_equipment_query
    stmt_args = (mob_id,)
    queue_transaction(mob_id, stmt, stmt_args)


def init_mob_equipment(db_row):
    if db_row:
        return MobEquipment(db_row[0], db_row[1], db_row[2])
    else:
        return None
