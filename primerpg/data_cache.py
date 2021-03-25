#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List, Optional

from primerpg.persistence.command_requirement_persistence import get_all_command_requirements
from primerpg.persistence.dto.command_requirement import CommandRequirement
from primerpg.persistence.dto.equipment_category import EquipmentCategory
from primerpg.persistence.dto.equipment_stat import EquipmentStat
from primerpg.persistence.dto.equipment_stat_category import EquipmentStatCategory
from primerpg.persistence.dto.item import Item
from primerpg.persistence.dto.item_category import ItemCategory
from primerpg.persistence.dto.player_state import PlayerState
from primerpg.persistence.dto.skill_category import SkillCategory
from primerpg.persistence.dto.task_category import TaskCategory
from primerpg.persistence.dto.zone import Zone
from primerpg.persistence.equipment_categories_persistence import get_all_equipment_categories
from primerpg.persistence.equipment_stat_categories_persistence import (
    get_all_equipment_stat_categories,
)
from primerpg.persistence.equipment_stat_persistence import get_all_equipment_stats
from primerpg.persistence.item_categories_persistence import get_all_item_categories
from primerpg.persistence.items_persistence import get_all_items
from primerpg.persistence.player_state_persistence import get_all_player_states
from primerpg.persistence.skill_category_persistence import get_all_skill_categories
from primerpg.persistence.task_category_persistence import get_all_task_categories
from primerpg.persistence.zone_persistence import get_all_zones

dne_string = "DNE"

# Preloaded data
command_requirements: List[CommandRequirement] = []
player_states: List[PlayerState] = []
task_categories: List[TaskCategory] = []
skill_categories: List[SkillCategory] = []
item_categories: List[ItemCategory] = []
equipment_stats: List[EquipmentStat] = []
equipment_categories: List[EquipmentCategory] = []
equipment_stat_categories: List[EquipmentStatCategory] = []
items: List[Item] = []
zones: List[Zone] = []


def load_util_data() -> None:
    global command_requirements, player_states, task_categories, skill_categories, equipment_categories
    global item_categories, equipment_stats, equipment_stat_categories, items, zones
    command_requirements = get_all_command_requirements()
    player_states = get_all_player_states()
    task_categories = get_all_task_categories()
    skill_categories = get_all_skill_categories()
    item_categories = get_all_item_categories()
    equipment_stats = get_all_equipment_stats()
    equipment_categories = get_all_equipment_categories()
    equipment_stat_categories = get_all_equipment_stat_categories()
    items = get_all_items()
    zones = get_all_zones()


# Command Requirement data helpers
def get_command_requirement_by_name(command_name: str) -> Optional[CommandRequirement]:
    """Gets the command requirement without hitting the database

    :param command_name: Name of the command to lookup
    :return: The CommandRequirement object associated with the name, or None if it does not exist
    """
    try:
        return next(filter(lambda req: req.name == command_name, command_requirements))
    except StopIteration:
        return None


# Task data helpers
def get_player_state_name(state_id: int) -> str:
    """Gets the player state name without hitting the database

    :param state_id: Unique id of the player state
    :return: The name of the player state, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda state: state.unique_id == state_id, player_states)).name
    except StopIteration:
        return dne_string


# Task Category data helpers
def get_task_category_name(task_id: int) -> str:
    """Gets the task category name without hitting the database

    :param task_id: Unique id of the task category
    :return: The name of the task category, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda task_cat: task_cat.unique_id == task_id, task_categories)).name
    except StopIteration:
        return dne_string


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


# Equipment Category data helpers
def get_equipment_category_name(equipment_category_id: int) -> str:
    """Gets the equipment category name without hitting the database

    :param equipment_category_id: Unique id of the stat category
    :return: The name of the equipment category, or "DNE" if it does not exist
    """
    try:
        return next(
            filter(
                lambda cat: cat.unique_id == equipment_category_id,
                equipment_categories,
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


def get_item_moveset_ids(item_id: int) -> [None, int]:
    """Gets the item moveset id without hitting the database

    :param item_id: Unique id of the item
    :return: The moveset id of the item, or None if it does not exist
    """
    try:
        return next(filter(lambda item: item.unique_id == item_id, items)).moveset_ids
    except StopIteration:
        return None


def get_item_category_id(item_id: int) -> [None, int]:
    """Gets the item category id without hitting the database

    :param item_id: Unique id of the item
    :return: The id of the item category, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda item: item.unique_id == item_id, items)).item_category_id
    except StopIteration:
        return None


# Zone data helpers
def get_zone_name(zone_id: int) -> str:
    """Gets the zone name without hitting the database

    :param zone_id: Unique id of the zone
    :return: The name of the zone, or "DNE" if it does not exist
    """
    try:
        return next(filter(lambda zone: zone.unique_id == zone_id, zones)).name
    except StopIteration:
        return dne_string
