from data.player_core import PlayerCore, idle_state, default_start_hp
from persistence.connection_handler import connection, queue_transaction

players_table = "players"

create_players_query = (
    "CREATE TABLE IF NOT EXISTS {0} ("
    "unique_id integer PRIMARY KEY, "
    "name text NOT NULL, "
    "avatar_url text NOT NULL, "
    "state text DEFAULT {1}, "
    "current_hp real DEFAULT {2})".format(players_table, idle_state, default_start_hp)
)
insert_players_query = (
    "INSERT INTO %s (unique_id, name, avatar_url) VALUES (?, ?, ?)" % players_table
)
update_players_query = (
    "UPDATE %s SET unique_id = ?, name = ?, avatar_url = ?, state = ?, current_hp = ? WHERE unique_id = ?"
    % players_table
)


def get_player(unique_id: int) -> PlayerCore:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = "SELECT * FROM %s WHERE unique_id=?" % players_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_player(result)


def insert_player_data(unique_id: int, name: str, avatar_url: str):
    stmt = insert_players_query
    stmt_args = (unique_id, name, avatar_url)
    queue_transaction(unique_id, stmt, stmt_args)


def update_player_data(player_core: PlayerCore):
    d = vars(player_core)
    stmt = update_players_query
    stmt_args = tuple(d.values()) + (player_core.unique_id,)
    queue_transaction(player_core.unique_id, stmt, stmt_args)


def init_player(db_row):
    if db_row:
        return PlayerCore(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4])
    else:
        return None
