from persistence.connection_handler import connection, process_queue
from persistence.item_categories_persistence import (
    populate_item_category_table,
    create_item_category_table,
)
from persistence.player_persistence import create_players_table
from persistence.task_persistence import create_player_tasks_table
from persistence.items_persistence import create_items_table, populate_item_table
from persistence.fish_persistence import create_fish_table, populate_fish_table
from persistence.inventory_persistence import create_inventory_table


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
    cursor_obj.execute(create_item_category_table)

    populate_fish_table()
    populate_item_table()
    populate_item_category_table()

    connection.commit()
