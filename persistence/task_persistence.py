from persistence.connection_handler import connection, queue_transaction
from persistence.dto.player_task import PlayerTask

player_tasks_table = "player_tasks"

select_player_tasks_query = "SELECT * FROM %s WHERE player_id = ?" % player_tasks_table
create_player_tasks_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "player_id integer PRIMARY KEY NOT NULL, "
    "task text NOT NULL, "
    "time_started text NOT NULL)" % player_tasks_table
)
insert_player_tasks_query = (
    "INSERT INTO %s (player_id, task, time_started) VALUES (?, ?, ?)"
    % player_tasks_table
)
delete_player_task_query = (
    "DELETE from %s WHERE player_id = ? AND task = ?" % player_tasks_table
)
delete_player_tasks_query = "DELETE from %s WHERE player_id = ?" % player_tasks_table


def get_player_task(unique_id: int) -> PlayerTask:
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_player_tasks_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_player_skill(result)


def insert_player_task(task: PlayerTask) -> None:
    stmt = insert_player_tasks_query
    stmt_args = (task.player_id, task.task, task.time_started)
    queue_transaction(task.player_id, stmt, stmt_args)


def delete_player_task(unique_id: int, task: str) -> None:
    stmt = delete_player_task_query
    stmt_args = (unique_id, task)
    queue_transaction(unique_id, stmt, stmt_args)


def delete_player_tasks(unique_id: int) -> None:
    stmt = delete_player_tasks_query
    stmt_args = (unique_id,)
    queue_transaction(unique_id, stmt, stmt_args)


def init_player_skill(db_row):
    if db_row:
        return PlayerTask(db_row[0], db_row[1], db_row[2])
    else:
        return None
