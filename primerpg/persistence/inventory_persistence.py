from typing import List

from primerpg.persistence.connection_handler import connection, queue_transaction
from primerpg.persistence.dto.player_inventory_item import PlayerInventoryItem

inventory_table = "inventory"

select_inventory_query = "SELECT * FROM %s WHERE player_id = ? AND item_id = ?" % inventory_table
select_all_inventory_query = "SELECT * FROM %s WHERE player_id = ?" % inventory_table
create_inventory_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "player_id integer NOT NULL, "
    "item_id integer NOT NULL, "
    "quantity integer NOT NULL, "
    "FOREIGN KEY(player_id) REFERENCES players(unique_id), "
    "FOREIGN KEY(item_id) REFERENCES items(unique_id))" % inventory_table
)
update_inventory_query = "UPDATE %s SET quantity = ? WHERE player_id = ? AND item_id = ?" % inventory_table
insert_inventory_query = "INSERT INTO %s (player_id, item_id, quantity) VALUES (?, ?, ?)" % inventory_table
delete_inventory_query = "DELETE from %s WHERE player_id = ?" % inventory_table


def get_inventory_item(player_id: int, item_id: int) -> PlayerInventoryItem:
    cursor_obj = connection.cursor()

    stmt_args = (
        player_id,
        item_id,
    )
    statement = select_inventory_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_inventory_item(result)


def get_all_inventory_items(player_id: int) -> List[PlayerInventoryItem]:
    cursor_obj = connection.cursor()

    stmt_args = (player_id,)
    statement = select_all_inventory_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_inventory_item(x) for x in result]

    return items


def insert_inventory_item(item: PlayerInventoryItem) -> None:
    stmt = insert_inventory_query
    stmt_args = (item.player_id, item.item_id, item.quantity)
    queue_transaction(item.player_id, stmt, stmt_args)


def update_inventory_item(item: PlayerInventoryItem) -> None:
    stmt = update_inventory_query
    stmt_args = (item.quantity, item.player_id, item.item_id)
    queue_transaction(item.player_id, stmt, stmt_args)


def delete_inventory_items(player_id: int) -> None:
    stmt = delete_inventory_query
    stmt_args = (player_id,)
    queue_transaction(player_id, stmt, stmt_args)


def init_inventory_item(db_row):
    if db_row:
        return PlayerInventoryItem(db_row[0], db_row[1], db_row[2])
    else:
        return None
