import sqlite3

players_table = 'players'
create_players_table = 'CREATE TABLE %s(id integer PRIMARY KEY, name text)' % players_table


def setup_db():
    create_tables()


def sql_connection():
    conn = sqlite3.connect('primeRPG.db')
    return conn


def create_tables(conn: sqlite3.Connection):
    cursor_obj = conn.cursor()

    cursor_obj.execute(create_players_table)

    conn.commit()


def get_player_data(conn: sqlite3.Connection, player_name: str):
    cursor_obj = conn.cursor()

    t = (player_name,)
    statement = 'SELECT * FROM %s WHERE symbol=?' % players_table
    cursor_obj.execute(statement, t)
    result = cursor_obj.fetchone()
    print(result)

    return result
