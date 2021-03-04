from data.item import Item
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
    "UPDATE %s SET quantity = ? WHERE player_id = ? AND item_id = ?" % inventory_table
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

    return init_item(result)


def get_all_inventory_data(player_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (player_id,)
    statement = select_inventory_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_item(x) for x in result]

    return items


def insert_inventory_data(item: Item):
    stmt = insert_inventory_table
    stmt_args = (item.player_id, item.item_id, item.quantity)
    queue_transaction(item.player_id, stmt, stmt_args)


def update_inventory_data(item: Item):
    stmt = update_inventory_table
    stmt_args = (item.quantity, item.player_id, item.item_id)
    queue_transaction(item.player_id, stmt, stmt_args)


def delete_inventory_data(player_id: int, item_id: int):
    stmt = delete_inventory_table
    stmt_args = (item_id,)
    queue_transaction(player_id, stmt, stmt_args)


def init_item(db_row):
    if db_row:
        return Item(db_row[0], db_row[1], db_row[2])
    else:
        return None
