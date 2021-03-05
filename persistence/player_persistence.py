import player
from persistence.connection_handler import connection, queue_transaction

players_table = "players"

create_players_table = (
    "CREATE TABLE IF NOT EXISTS {0} "
    "(unique_id integer PRIMARY KEY, name text NOT NULL, state text DEFAULT {1})".format(
        players_table, player.idle_state
    )
)
insert_players_table = "INSERT INTO %s (unique_id, name) VALUES (?, ?)" % players_table
update_players_table = (
    "UPDATE %s SET unique_id = ?, name = ?, state = ? WHERE unique_id = ?"
    % players_table
)


def get_player(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = "SELECT * FROM %s WHERE unique_id=?" % players_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    if result is None:
        return None

    return player.Player(result[0], result[1], result[2])


def insert_player_data(unique_id: int, name: str):
    stmt = insert_players_table
    stmt_args = (unique_id, name)
    queue_transaction(unique_id, stmt, stmt_args)


def update_player_data(unique_id: int, player_dict: dict):
    stmt = update_players_table
    stmt_args = tuple(player_dict.values()) + (unique_id,)
    queue_transaction(unique_id, stmt, stmt_args)
