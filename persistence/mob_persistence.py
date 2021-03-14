import json

from consts import data_folder
from persistence.common_persistence import insert_dictionary
from persistence.connection_handler import connection
from persistence.dto.mob_core import MobCore

mobs_table = "mobs"

select_mobs_query = "SELECT * FROM %s WHERE unique_id = ?" % mobs_table
create_mobs_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "unique_id integer PRIMARY KEY NOT NULL,"
    "name text NOT NULL,"
    "base_xp integer NOT NULL,"
    "icon_url text NOT NULL)" % mobs_table
)


def populate_mobs_table():
    with open(data_folder / "mobs.json") as f:
        data = json.load(f)

    for mob in data:
        if not get_mob(mob["unique_id"]):
            del mob["skills"]
            del mob["equipment"]
            del mob["drops"]
            insert_dictionary(mobs_table, mob)


def get_mob(unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = select_mobs_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob(result)


def init_mob(db_row):
    if db_row:
        return MobCore(
            db_row[0],
            db_row[1],
            db_row[2],
            db_row[3],
        )
    else:
        return None
