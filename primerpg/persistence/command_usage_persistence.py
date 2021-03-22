#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from primerpg.persistence.connection_handler import connection, queue_transaction
from primerpg.persistence.dto.command_usage import CommandUsage

file_name = "command_usages.json"
command_usages_table = "command_usages"

select_command_usage_query = "SELECT * FROM %s WHERE player_id = ? AND command_id = ?" % command_usages_table
select_all_command_usages_query = "SELECT * FROM %s" % command_usages_table
create_command_usages_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "player_id integer NOT NULL, "
    "command_id integer NOT NULL, "
    "time_last_used integer NOT NULL, "
    "PRIMARY KEY(player_id, command_id), "
    "FOREIGN KEY(player_id) REFERENCES players(unique_id), "
    "FOREIGN KEY(command_id) REFERENCES command_requirements(unique_id))" % command_usages_table
)
insert_command_usage_query = (
    "INSERT INTO %s (player_id, command_id, time_last_used) VALUES (?, ?, ?)" % command_usages_table
)
update_command_usage_query = (
    "UPDATE %s SET time_last_used = ? WHERE player_id = ? AND command_id = ?" % command_usages_table
)
delete_command_usage_query = "DELETE from %s WHERE player_id = ? AND command_id = ?" % command_usages_table


def get_command_usage(player_id: int, command_id: int) -> CommandUsage:
    cursor_obj = connection.cursor()

    stmt_args = (player_id, command_id)
    statement = select_command_usage_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_command_usage(result)


def get_all_command_usages() -> List[CommandUsage]:
    cursor_obj = connection.cursor()

    statement = select_all_command_usages_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_command_usage(r) for r in result]


def insert_command_usage(command_usage: CommandUsage) -> None:
    stmt = insert_command_usage_query
    stmt_args = (command_usage.player_id, command_usage.command_id, command_usage.time_last_used)
    queue_transaction(command_usage.player_id, stmt, stmt_args)


def update_command_usage(command_usage: CommandUsage) -> None:
    stmt = update_command_usage_query
    stmt_args = (command_usage.time_last_used, command_usage.player_id, command_usage.command_id)
    queue_transaction(command_usage.player_id, stmt, stmt_args)


def delete_command_usage(player_id: int, command_id: int) -> None:
    stmt = delete_command_usage_query
    stmt_args = (player_id, command_id)
    queue_transaction(player_id, stmt, stmt_args)


def init_command_usage(db_row):
    if db_row:
        return CommandUsage(
            db_row[0],
            db_row[1],
            db_row[2],
        )
    else:
        return None
