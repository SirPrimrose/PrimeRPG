#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List, Optional

from primerpg.persistence.dto.equipment_stat import EquipmentStat
from primerpg.persistence.dto.equipment_stat_category import EquipmentStatCategory
from primerpg.persistence.dto.item import Item
from primerpg.persistence.dto.item_category import ItemCategory
from primerpg.persistence.dto.skill_category import SkillCategory
from primerpg.persistence.equipment_stat_categories_persistence import (
    get_all_equipment_stat_categories,
)
from primerpg.persistence.equipment_stat_persistence import get_all_equipment_stats
from primerpg.persistence.item_categories_persistence import get_all_item_categories
from primerpg.persistence.items_persistence import get_all_items
from primerpg.persistence.skill_category_persistence import get_all_skill_categories

dne_string = "DNE"

# Preloaded data
skill_categories: List[SkillCategory] = []
item_categories: List[ItemCategory] = []
equipment_stats: List[EquipmentStat] = []
equipment_stat_categories: List[EquipmentStatCategory] = []
items: List[Item] = []


def load_util_data() -> None:
    global skill_categories, item_categories, equipment_stats, equipment_stat_categories, items
    skill_categories = get_all_skill_categories()
    item_categories = get_all_item_categories()
    equipment_stats = get_all_equipment_stats()
    equipment_stat_categories = get_all_equipment_stat_categories()
    items = get_all_items()


# Skill Category data helpers
def get_skill_category_name(skill_id: int) -> str:
    """Gets the skill category name without hitting the database

    :param skill_id: Unique id of the skill category
    :return: The name of the skill category, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda skill_cat: skill_cat.unique_id == skill_id, skill_categories)).name
    except StopIteration:
        return dne_string


def get_skill_category_short_name(skill_id: int) -> str:
    """Gets the skill category short name without hitting the database

    :param skill_id: Unique id of the skill category
    :return: The short name of the skill category, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda skill_cat: skill_cat.unique_id == skill_id, skill_categories)).short_name
    except StopIteration:
        return dne_string


# Item Category data helpers
def get_item_category_name(item_cat_id: int) -> str:
    """Gets the item category name without hitting the database

    :param item_cat_id: Unique id of the item
    :return: The name of the item category, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda item_cat: item_cat.unique_id == item_cat_id, item_categories)).name
    except StopIteration:
        return dne_string


# Equipment Stat data helpers
def get_equipment_stat(item_id: int, equipment_stat_category_id: int) -> Optional[EquipmentStat]:
    """Gets the equipment stat without hitting the database

    :param item_id: Item id of the stat
    :param equipment_stat_category_id: Category id of the stat
    :return: The EquipmentStat object, or None if it does not exist
    """
    try:
        return next(
            filter(
                lambda eq_stat: eq_stat.item_id == item_id
                and eq_stat.equipment_stat_category_id == equipment_stat_category_id,
                equipment_stats,
            )
        )
    except StopIteration:
        return None


# Equipment Stat Category data helpers
def get_equipment_stat_category_name(equipment_stat_category_id: int) -> str:
    """Gets the equipment stat category name without hitting the database

    :param equipment_stat_category_id: Unique id of the stat category
    :return: The name of the equipment stat category, or "DNE" if it does not exist
    """
    try:
        return next(
            filter(
                lambda cat: cat.unique_id == equipment_stat_category_id,
                equipment_stat_categories,
            )
        ).name
    except StopIteration:
        return dne_string


# Item data helpers
def get_item_id(item_name: str) -> [None, int]:
    """Gets the item id without hitting the database

    :param item_name: Name of the item, case insensitive
    :return: The id of the item, or None if it does not exist
    """
    try:
        return next(filter(lambda item: item.name.lower() == item_name.lower(), items)).unique_id
    except StopIteration:
        return None


def get_item_name(item_id: int) -> str:
    """Gets the item name without hitting the database

    :param item_id: Unique id of the item
    :return: The name of the item, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda item: item.unique_id == item_id, items)).name
    except StopIteration:
        return dne_string


def get_item_category_id(item_id: int) -> [None, int]:
    """Gets the item category id without hitting the database

    :param item_id: Unique id of the item
    :return: The id of the item category, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda item: item.unique_id == item_id, items)).item_category_id
    except StopIteration:
        return None
