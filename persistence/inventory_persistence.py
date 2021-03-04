from persistence.connection_handler import connection, queue_transaction

inventory_table = "inventory"

select_inventory_table = (
    "SELECT * FROM %s WHERE player_id = ? AND item_id = ?" % inventory_table
)
select_all_inventory_table = "SELECT * FROM %s WHERE player_id = ?" % inventory_table
create_inventory_table = (
    "CREATE TABLE IF NOT EXISTS %s"
    " (player_id integer, item_id integer, quantity integer)" % inventory_table
)
update_inventory_table = (
    "UPDATE %s SET quantity =? WHERE player_id = ? AND item_id = ?" % inventory_table
)
insert_inventory_table = (
    "INSERT INTO %s (player_id, item_id, quantity) VALUES (?, ?, ?)" % inventory_table
)
delete_inventory_table = "DELETE from %s WHERE player_id = ?"


def get_inventory_data(player_id: int, item_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (
        player_id,
        item_id,
    )
    statement = select_inventory_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def get_all_inventory_data(player_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (player_id,)
    statement = select_inventory_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    return result


def insert_inventory_data(player_id: int, item_id: int, quantity):
    stmt = insert_inventory_table
    stmt_args = (item_id, quantity)
    queue_transaction(player_id, stmt, stmt_args)


def update_inventory_data(player_id: int, item_id: int, quantity: int):
    stmt = insert_inventory_table
    stmt_args = (player_id, item_id, quantity)
    queue_transaction(player_id, stmt, stmt_args)


def delete_inventory_data(player_id: int, item_id: int):
    stmt = delete_inventory_table
    stmt_args = (item_id,)
    queue_transaction(player_id, stmt, stmt_args)
