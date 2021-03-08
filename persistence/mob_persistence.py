import json

from consts import data_folder
from data.mob_core import MobCore
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection

mobs_table = "mobs"

select_mobs_table = "SELECT * FROM %s WHERE unique_id = ?" % mobs_table
create_mobs_table = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL,"
    "name text NOT NULL,"
    "base_xp integer NOT NULL)" % mobs_table
)


def populate_mobs_table():
    with open(data_folder / "mobs.json") as f:
        data = json.load(f)

    for mob in data:
        if not get_mob(mob["unique_id"]):
            del mob["skills"]
            del mob["equipment"]
            insert_dictionary(mobs_table, mob)


def get_mob(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_mobs_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob(result)


def init_mob(db_row):
    if db_row:
        return MobCore(
            db_row[0],
            db_row[1],
            db_row[2],
        )
    else:
        return None