import sqlite3

# Table Names
players_table = 'players'

# Queries
create_players_table = 'CREATE TABLE IF NOT EXISTS %s(unique_id integer PRIMARY KEY, name text)' % players_table
insert_players_table = 'INSERT INTO %s (unique_id, name) VALUES (?, ?)' % players_table

# Open connection to database
connection = sqlite3.connect('primeRPG.db')


def setup_db():
    create_tables()


def create_tables():
    cursor_obj = connection.cursor()

    cursor_obj.execute(create_players_table)

    connection.commit()


def get_player_data(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = 'SELECT * FROM %s WHERE unique_id=?' % players_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def create_player_data(unique_id: int, name: str):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id, name)
    cursor_obj.execute(insert_players_table, stmt_args)

    connection.commit()
