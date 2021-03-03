import json
import sqlite3

import player

# Table Names
players_table = 'players'
player_tasks_table = 'player_tasks'
fish_table = 'fish'

# Queries
create_players_table = 'CREATE TABLE IF NOT EXISTS {0} ' \
                       '(unique_id integer PRIMARY KEY, name text, state text DEFAULT {1})' \
    .format(players_table, player.idle_state)
insert_players_table = 'INSERT INTO %s (unique_id, name) VALUES (?, ?)' % players_table
update_players_table = 'UPDATE %s SET unique_id = ?, name = ?, state = ? WHERE unique_id = ?' % players_table

create_player_tasks_table = 'CREATE TABLE IF NOT EXISTS %s' \
                            ' (unique_id integer, task text, time_started text)' % player_tasks_table

create_fish_table = 'CREATE TABLE IF NOT EXISTS %s' \
                    ' (unique_id integer, name text, start_time text, end_time text, weather text, weight int)' \
                    % fish_table

# Open connection to database
connection = sqlite3.connect('primeRPG.db')


def setup_db():
    create_tables()


def create_tables():
    cursor_obj = connection.cursor()

    cursor_obj.execute(create_players_table)
    cursor_obj.execute(create_player_tasks_table)
    cursor_obj.execute(create_fish_table)

    populate_fish_table()

    connection.commit()


def populate_fish_table():
    with open('data/fish.json') as f:
        data = json.load(f)

    for fish in data:
        if not get_dictionary_from_table(fish_table, fish['unique_id']):
            insert_dictionary(fish_table, fish)

    connection.commit()


def get_player_data(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = 'SELECT * FROM %s WHERE unique_id=?' % players_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    if result is None:
        return None

    p = player.Player(result[0], result[1], result[2])

    return p


def create_player_data(unique_id: int, name: str):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id, name)
    cursor_obj.execute(insert_players_table, stmt_args)

    connection.commit()


def update_player_data(unique_id: int, player_dict: dict):
    cursor_obj = connection.cursor()

    stmt_args = tuple(player_dict.values()) + (unique_id,)
    statement = update_players_table
    cursor_obj.execute(statement, stmt_args)

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
