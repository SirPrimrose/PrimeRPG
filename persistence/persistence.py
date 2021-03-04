from persistence.connection_handler import connection, process_queue
from persistence.player_persistence import create_players_table
from persistence.task_persistence import create_player_tasks_table
from persistence.items_persistence import create_items_table
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

    populate_fish_table()

    connection.commit()

