from persistence.connection_handler import connection, process_queue
from persistence.equipment_categories_persistence import (
    create_equipment_categories_table,
    populate_equipment_categories_table,
)
from persistence.fish_persistence import create_fish_table, populate_fish_table
from persistence.inventory_persistence import create_inventory_table
from persistence.item_categories_persistence import (
    populate_item_categories_table,
    create_item_categories_table,
)
from persistence.items_persistence import create_items_table, populate_items_table
from persistence.player_persistence import create_players_table
from persistence.player_skill_persistence import create_player_skills_table
from persistence.skill_categories_persistence import (
    create_skill_categories_table,
    populate_skill_categories_table,
)
from persistence.task_persistence import create_player_tasks_table


def setup_db():
    create_tables()


def save_queue():
    process_queue()


def create_tables():
    cursor_obj = connection.cursor()

    cursor_obj.execute(create_players_table)
    cursor_obj.execute(create_player_tasks_table)
    cursor_obj.execute(create_fish_table)
    cursor_obj.execute(create_items_table)
    cursor_obj.execute(create_inventory_table)
    cursor_obj.execute(create_item_categories_table)
    cursor_obj.execute(create_equipment_categories_table)
    cursor_obj.execute(create_skill_categories_table)
    cursor_obj.execute(create_player_skills_table)

    populate_fish_table()
    populate_items_table()
    populate_item_categories_table()
    populate_equipment_categories_table()
    populate_skill_categories_table()

    connection.commit()
