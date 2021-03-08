import sys
from sqlite3 import OperationalError, IntegrityError
from traceback import print_exc
from typing import List

from data.equipment_category import EquipmentCategory
from data.item import Item
from data.skill_category import SkillCategory
from persistence.connection_handler import connection


def get_dictionary_from_table(table_name: str, unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = "SELECT * FROM %s WHERE unique_id = ?" % table_name
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def insert_dictionary(table_name: str, my_dict: dict):
    cursor_obj = connection.cursor()
    placeholders = ", ".join(["?"] * len(my_dict))
    columns = ", ".join(my_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)
    try:
        cursor_obj.execute(sql, list(my_dict.values()))
    except OperationalError:
        print_exc()
        print("Encountered error: {0}".format(sys.exc_info()[1]))
    except IntegrityError:
        print("Integrity error: {0}".format(sys.exc_info()[1]))
        print("Tried to insert {} into table {}".format(my_dict, table_name))


def convert_skill_names_to_id(skill_categories: List[SkillCategory], skills: dict):
    new_skills = {}
    for skill_name, scaling in skills.items():
        category = next(
            filter(lambda cat: cat.name == skill_name, skill_categories), None
        )
        new_skills[category.unique_id] = scaling
    return new_skills


def convert_equipment_slot_names_to_id(
    equipment_categories: List[EquipmentCategory], equipment: dict
):
    new_equipment = {}
    for equipment_name, item_name in equipment.items():
        category = next(
            filter(lambda cat: cat.name == equipment_name, equipment_categories), None
        )
        new_equipment[category.unique_id] = item_name
    return new_equipment


def convert_item_names_to_id(items: List[Item], equipment: dict):
    new_equipment = {}
    for equipment_name, item_name in equipment.items():
        item = next(filter(lambda cat: cat.name == item_name, items), None)
        new_equipment[equipment_name] = item.unique_id
    return new_equipment
