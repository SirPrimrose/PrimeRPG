import json
from typing import List

from consts import data_folder
from data.equipment_stat import EquipmentStat
from persistence.common_persistence import insert_dictionary, convert_skill_names_to_id
from persistence.connection_handler import connection
from persistence.skill_categories_persistence import get_all_skill_categories

equipment_stats_table = "equipment_stats"

select_equipment_stat_table = (
    "SELECT * FROM %s WHERE item_id = ? AND equipment_stat_category_id = ?"
    % equipment_stats_table
)
select_equipment_stats_table = (
    "SELECT * FROM %s WHERE item_id = ?" % equipment_stats_table
)
create_equipment_stats_table = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "item_id integer NOT NULL, "
    "equipment_stat_category_id integer NOT NULL, "
    "value integer NOT NULL, "
    "scales_with text NOT NULL, "
    "PRIMARY KEY(item_id, equipment_stat_category_id), "
    "FOREIGN KEY(item_id) REFERENCES items(unique_id), "
    "FOREIGN KEY(equipment_stat_category_id) REFERENCES equipment_stat_categories(unique_id))"
    % equipment_stats_table
)


def populate_equipment_stats_table():
    with open(data_folder / "equipment_stats.json") as f:
        data = json.load(f)

    skill_categories = get_all_skill_categories()
    for item in data:
        for stat in item["stats"]:
            if not get_equipment_stat(
                item["item_id"], stat["equipment_stat_category_id"]
            ):
                new_scalings = convert_skill_names_to_id(
                    skill_categories, stat["scales_with"]
                )
                stat.update(
                    {"scales_with": str(new_scalings), "item_id": item["item_id"]}
                )
                insert_dictionary(equipment_stats_table, stat)


def get_equipment_stat(item_id: int, equipment_stat_category_id: int) -> EquipmentStat:
    cursor_obj = connection.cursor()

    stmt_args = (item_id, equipment_stat_category_id)
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
            dict(db_row[3]),
        )
    else:
        return None
