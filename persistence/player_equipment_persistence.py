from typing import List

from persistence.connection_handler import connection, queue_transaction
from persistence.dto.player_equipment import PlayerEquipment

player_equipment_table = "player_equipment"

select_player_equipment_query = (
    "SELECT * FROM %s WHERE player_id = ? AND equipment_category_id = ?"
    % player_equipment_table
)
select_all_player_equipment_query = (
    "SELECT * FROM %s WHERE player_id = ?" % player_equipment_table
)
create_player_equipment_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "player_id integer NOT NULL, "
    "equipment_category_id integer NOT NULL, "
    "item_id integer NOT NULL)" % player_equipment_table
)
update_player_equipment_query = (
    "UPDATE %s SET item_id = ? WHERE player_id = ? AND equipment_category_id = ?"
    % player_equipment_table
)
insert_player_equipment_query = (
    "INSERT INTO %s (player_id, equipment_category_id, item_id) VALUES (?, ?, ?)"
    % player_equipment_table
)
delete_player_equipment_query = (
    "DELETE from %s WHERE player_id = ?" % player_equipment_table
)


def get_player_equipment(player_id: int, equipment_category_id: int) -> PlayerEquipment:
    cursor_obj = connection.cursor()

    stmt_args = (
        player_id,
        equipment_category_id,
    )
    statement = select_player_equipment_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_player_equipment(result)


def get_all_player_equipment(player_id: int) -> List[PlayerEquipment]:
    cursor_obj = connection.cursor()

    stmt_args = (player_id,)
    statement = select_all_player_equipment_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    return [init_player_equipment(x) for x in result]


def insert_player_equipment(equipment: PlayerEquipment):
    stmt = insert_player_equipment_query
    stmt_args = (
        equipment.get_player_id(),
        equipment.equipment_category_id,
        equipment.item_id,
    )
    queue_transaction(equipment.get_player_id(), stmt, stmt_args)


def update_player_equipment(equipment: PlayerEquipment):
    stmt = update_player_equipment_query
    stmt_args = (
        equipment.item_id,
        equipment.get_player_id(),
        equipment.equipment_category_id,
    )
    queue_transaction(equipment.get_player_id(), stmt, stmt_args)


def delete_player_equipment(player_id: int):
    stmt = delete_player_equipment_query
    stmt_args = (player_id,)
    queue_transaction(player_id, stmt, stmt_args)


def init_player_equipment(db_row):
    if db_row:
        return PlayerEquipment(db_row[0], db_row[1], db_row[2])
    else:
        return None
