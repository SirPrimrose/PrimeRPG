import json
from datetime import timedelta

import util
from data.fish import Fish
from persistence.connection_handler import connection
from persistence.persistence import insert_dictionary, get_dictionary_from_table, data_folder

fish_table = 'fish'

create_fish_table = 'CREATE TABLE IF NOT EXISTS %s' \
                    ' (unique_id integer, name text, start_time text, end_time text, weather text, weight int)' \
                    % fish_table
select_fish_table = 'SELECT * FROM %s WHERE datetime(start_time) <= datetime(?) AND datetime(end_time) >= datetime(' \
                    '?) AND weather = \'both\' OR weather = ?' % fish_table


def populate_fish_table():
    with open(data_folder / 'fish.json') as f:
        data = json.load(f)

    for fish in data:
        if not get_dictionary_from_table(fish_table, fish['unique_id']):
            insert_dictionary(fish_table, fish)

    connection.commit()


def get_fish_data(time_d: timedelta, weather: str):
    cursor_obj = connection.cursor()

    time_str = util.time_delta_to_str(time_d)
    stmt_args = (time_str, time_str, weather)
    statement = select_fish_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    fish = [init_fish(x) for x in result]

    return fish


def init_fish(db_row):
    return Fish(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5])
