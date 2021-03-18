#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import json
from typing import List

from primerpg.consts import data_folder
from primerpg.data.entity_skill import EntitySkill
from primerpg.persistence.common_persistence import convert_dict_keys_to_id, insert_dictionary
from primerpg.persistence.connection_handler import connection, queue_transaction
from primerpg.persistence.skill_categories_persistence import get_all_skill_categories
from primerpg.util import req_xp_for_level

mob_skills_table = "mob_skills"

select_mob_skills_query = "SELECT * FROM %s WHERE mob_id = ? AND skill_id = ?" % mob_skills_table
select_all_mob_skills_query = "SELECT * FROM %s WHERE mob_id = ?" % mob_skills_table
create_mob_skills_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "mob_id integer NOT NULL, "
    "skill_id integer NOT NULL, "
    "total_xp integer NOT NULL, "
    "PRIMARY KEY(mob_id, skill_id))" % mob_skills_table
)
update_mob_skills_query = "UPDATE %s SET total_xp = ? WHERE mob_id = ? AND skill_id = ?" % mob_skills_table
insert_mob_skills_query = "INSERT INTO %s (mob_id, skill_id, total_xp) VALUES (?, ?, ?)" % mob_skills_table
delete_mob_skills_query = "DELETE from %s WHERE mob_id = ?" % mob_skills_table


def populate_mob_skills_table():
    with open(data_folder / "mobs.json") as f:
        data = json.load(f)

    skill_categories = get_all_skill_categories()
    for mob in data:
        skills = convert_dict_keys_to_id(skill_categories, mob["skills"])
        for skill_id, skill_value in skills.items():
            if not get_mob_skill(mob["unique_id"], skill_id):
                mob_skill = {
                    "mob_id": mob["unique_id"],
                    "skill_id": skill_id,
                    "total_xp": req_xp_for_level(skill_value),
                }
                insert_dictionary(mob_skills_table, mob_skill)


def get_mob_skill(mob_id: int, skill_id: int) -> EntitySkill:
    cursor_obj = connection.cursor()

    stmt_args = (
        mob_id,
        skill_id,
    )
    statement = select_mob_skills_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob_skill(result)


def get_all_mob_skills(mob_id: int) -> List[EntitySkill]:
    cursor_obj = connection.cursor()

    stmt_args = (mob_id,)
    statement = select_all_mob_skills_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_mob_skill(x) for x in result]

    return items


def insert_mob_skill(skill: EntitySkill):
    stmt = insert_mob_skills_query
    stmt_args = (skill.entity_id, skill.skill_id, skill.get_total_xp())
    queue_transaction(skill.entity_id, stmt, stmt_args)


def update_mob_skill(skill: EntitySkill):
    stmt = update_mob_skills_query
    stmt_args = (skill.get_total_xp(), skill.entity_id, skill.skill_id)
    queue_transaction(skill.entity_id, stmt, stmt_args)


def delete_mob_skills(mob_id: int):
    stmt = delete_mob_skills_query
    stmt_args = (mob_id,)
    queue_transaction(mob_id, stmt, stmt_args)


def init_mob_skill(db_row):
    if db_row:
        return EntitySkill(db_row[0], db_row[1], db_row[2])
    else:
        return None
