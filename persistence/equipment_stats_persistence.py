import json
from typing import List

from consts import data_folder
from data.equipment_stat import EquipmentStat
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection

equipment_stats_table = "equipment_stats"

select_equipment_stat_table = (
    "SELECT * FROM %s WHERE item_id = ? AND skill_category_id = ?"
    % equipment_stats_table
)
select_equipment_stats_table = (
    "SELECT * FROM %s WHERE item_id = ?" % equipment_stats_table
)
create_equipment_stats_table = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "item_id integer NOT NULL, "
    "skill_category_id integer NOT NULL, "
    "scaling integer NOT NULL, "
    "bonus integer NOT NULL, "
    "PRIMARY KEY(item_id, skill_category_id), "
    "FOREIGN KEY(item_id) REFERENCES items(unique_id), "
    "FOREIGN KEY(skill_category_id) REFERENCES skill_categories(unique_id))"
    % equipment_stats_table
)


def populate_equipment_stats_table():
    with open(data_folder / "equipment_stats.json") as f:
        data = json.load(f)

    for item in data:
        for skill in item["skills"]:
            if not get_equipment_stat(item["item_id"], skill["skill_category_id"]):
                skill.update({"item_id": item["item_id"]})
                insert_dictionary(equipment_stats_table, skill)


def get_equipment_stat(item_id: int, skill_category_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (item_id, skill_category_id)
    statement = select_equipment_stat_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def get_equipment_stats(item_id: int) -> List[EquipmentStat]:
    cursor_obj = connection.cursor()

    stmt_args = (item_id,)
    statement = select_equipment_stats_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    return [init_equipment_stat(r) for r in result]


def init_equipment_stat(db_row):
    if db_row:
        return EquipmentStat(
            db_row[0],
            db_row[1],
            db_row[2],
            db_row[3],
        )
    else:
        return None
