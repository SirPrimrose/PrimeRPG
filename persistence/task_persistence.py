from persistence.connection_handler import connection, queue_transaction

player_tasks_table = "player_tasks"

select_player_tasks_query = "SELECT * FROM %s WHERE unique_id = ?" % player_tasks_table
create_player_tasks_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL, "
    "task text NOT NULL, "
    "time_started text NOT NULL)" % player_tasks_table
)
insert_player_tasks_query = (
    "INSERT INTO %s (unique_id, task, time_started) VALUES (?, ?, ?)"
    % player_tasks_table
)
delete_player_tasks_query = (
    "DELETE from %s WHERE unique_id = ? AND task = ?" % player_tasks_table
)


def get_player_task_data(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_player_tasks_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def insert_player_task_data(unique_id: int, task: str, time: str):
    stmt = insert_player_tasks_query
    stmt_args = (unique_id, task, time)
    queue_transaction(unique_id, stmt, stmt_args)


def delete_player_task_data(unique_id: int, task: str):
    stmt = delete_player_tasks_query
    stmt_args = (unique_id, task)
    queue_transaction(unique_id, stmt, stmt_args)
