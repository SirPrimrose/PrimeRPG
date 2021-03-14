from typing import List

from persistence.connection_handler import connection, queue_transaction
from persistence.dto.player_core import PlayerCore

players_table = "players"

create_players_query = (
    "CREATE TABLE IF NOT EXISTS {0} ("
    "unique_id integer PRIMARY KEY, "
    "name text NOT NULL, "
    "avatar_url text NOT NULL, "
    "state text NOT NULL, "
    "current_hp real NOT NULL, "
    "hp_regen real NOT NULL)".format(players_table)
)
insert_players_query = (
    "INSERT INTO %s (unique_id, name, avatar_url, state, current_hp, hp_regen) VALUES (?, ?, ?, ?, ?, ?)"
    % players_table
)
update_players_query = (
    "UPDATE %s SET name = ?, avatar_url = ?, state = ?, current_hp = ?, hp_regen = ? WHERE unique_id = ?"
    % players_table
)
delete_players_query = "DELETE from %s WHERE unique_id = ?" % players_table


def get_player(unique_id: int) -> PlayerCore:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = "SELECT * FROM %s WHERE unique_id=?" % players_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_player(result)


def get_all_players() -> List[PlayerCore]:
    cursor_obj = connection.cursor()

    statement = "SELECT * FROM %s" % players_table
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_player(r) for r in result]


def insert_player_data(player_core: PlayerCore):
    stmt = insert_players_query
    stmt_args = (
        player_core.unique_id,
        player_core.name,
        player_core.avatar_url,
        player_core.state,
        player_core.current_hp,
        player_core.hp_regen,
    )
    queue_transaction(player_core.unique_id, stmt, stmt_args)


def update_player_data(player_core: PlayerCore, quiet=False):
    stmt = update_players_query
    stmt_args = (
        player_core.name,
        player_core.avatar_url,
        player_core.state,
        player_core.current_hp,
        player_core.hp_regen,
        player_core.unique_id,
    )
    queue_transaction(player_core.unique_id if not quiet else None, stmt, stmt_args)


def delete_player_data(player_id: int):
    stmt = delete_players_query
    stmt_args = (player_id,)
    queue_transaction(player_id, stmt, stmt_args)


def init_player(db_row):
    if db_row:
        return PlayerCore(
            db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5]
        )
    else:
        return None
