from pathlib import Path

from persistence.connection_handler import connection, process_queue
from persistence.player_persistence import create_players_table
from persistence.task_persistence import create_player_tasks_table
from persistence.items_persistence import create_items_table
from persistence.fish_persistence import create_fish_table, populate_fish_table
from persistence.inventory_persistence import create_inventory_table

data_folder = Path("data")


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


def get_dictionary_from_table(table_name: str, unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = 'SELECT * FROM %s WHERE unique_id = ?' % table_name
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def insert_dictionary(table_name: str, my_dict: dict):
    cursor_obj = connection.cursor()
    placeholders = ', '.join(['?'] * len(my_dict))
    columns = ', '.join(my_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)
    cursor_obj.execute(sql, list(my_dict.values()))
