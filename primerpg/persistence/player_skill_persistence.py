#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from primerpg.data.entity_skill import EntitySkill
from primerpg.persistence.connection_handler import connection, queue_transaction

player_skills_table = "player_skills"

select_player_skills_query = "SELECT * FROM %s WHERE player_id = ? AND skill_id = ?" % player_skills_table
select_all_player_skills_query = "SELECT * FROM %s WHERE player_id = ?" % player_skills_table
create_player_skills_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "player_id integer NOT NULL, "
    "skill_id integer NOT NULL, "
    "total_xp integer NOT NULL, "
    "PRIMARY KEY(player_id, skill_id))" % player_skills_table
)
update_player_skills_query = "UPDATE %s SET total_xp = ? WHERE player_id = ? AND skill_id = ?" % player_skills_table
insert_player_skills_query = "INSERT INTO %s (player_id, skill_id, total_xp) VALUES (?, ?, ?)" % player_skills_table
delete_player_skills_query = "DELETE from %s WHERE player_id = ?" % player_skills_table


def get_player_skill(player_id: int, skill_id: int) -> EntitySkill:
    cursor_obj = connection.cursor()

    stmt_args = (
        player_id,
        skill_id,
    )
    statement = select_player_skills_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_player_skill(result)


def get_all_player_skills(player_id: int) -> List[EntitySkill]:
    cursor_obj = connection.cursor()

    stmt_args = (player_id,)
    statement = select_all_player_skills_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_player_skill(x) for x in result]

    return items


def insert_player_skill(skill: EntitySkill):
    stmt = insert_player_skills_query
    stmt_args = (skill.entity_id, skill.skill_id, skill.get_total_xp())
    queue_transaction(skill.entity_id, stmt, stmt_args)


def update_player_skill(skill: EntitySkill):
    stmt = update_player_skills_query
    stmt_args = (skill.get_total_xp(), skill.entity_id, skill.skill_id)
    queue_transaction(skill.entity_id, stmt, stmt_args)


def delete_player_skills(player_id: int):
    stmt = delete_player_skills_query
    stmt_args = (player_id,)
    queue_transaction(player_id, stmt, stmt_args)


def init_player_skill(db_row):
    if db_row:
        return EntitySkill(db_row[0], db_row[1], db_row[2])
    else:
        return None
