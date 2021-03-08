import json
from typing import List

from consts import data_folder
from data.mob_skill import MobSkill
from persistence.common_persistence import insert_dictionary, convert_skill_names_to_id
from persistence.connection_handler import connection, queue_transaction
from persistence.skill_categories_persistence import get_all_skill_categories

mob_skills_table = "mob_skills"

select_mob_skills_table = (
    "SELECT * FROM %s WHERE mob_id = ? AND skill_id = ?" % mob_skills_table
)
select_all_mob_skills_table = "SELECT * FROM %s WHERE mob_id = ?" % mob_skills_table
create_mob_skills_table = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "mob_id integer NOT NULL, "
    "skill_id integer NOT NULL, "
    "total_xp integer NOT NULL, "
    "PRIMARY KEY(mob_id, skill_id))" % mob_skills_table
)
update_mob_skills_table = (
    "UPDATE %s SET total_xp = ? WHERE mob_id = ? AND skill_id = ?" % mob_skills_table
)
insert_mob_skills_table = (
    "INSERT INTO %s (mob_id, skill_id, total_xp) VALUES (?, ?, ?)" % mob_skills_table
)
delete_mob_skills_table = "DELETE from %s WHERE mob_id = ?"


def populate_mob_skills_table():
    with open(data_folder / "mobs.json") as f:
        data = json.load(f)

    skill_categories = get_all_skill_categories()
    for mob in data:
        new_skills = convert_skill_names_to_id(skill_categories, mob["skills"])
        for skill_id, skill_value in new_skills.items():
            if not get_mob_skill(mob["unique_id"], skill_id):
                mob_skill = {
                    "mob_id": mob["unique_id"],
                    "skill_id": skill_id,
                    "total_xp": skill_value,
                }
                insert_dictionary(mob_skills_table, mob_skill)


def get_mob_skill(mob_id: int, skill_id: int) -> MobSkill:
    cursor_obj = connection.cursor()

    stmt_args = (
        mob_id,
        skill_id,
    )
    statement = select_mob_skills_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_mob_skill(result)


def get_all_mob_skills(mob_id: int) -> List[MobSkill]:
    cursor_obj = connection.cursor()

    stmt_args = (mob_id,)
    statement = select_all_mob_skills_table
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_mob_skill(x) for x in result]

    return items


def insert_mob_skill(skill: MobSkill):
    stmt = insert_mob_skills_table
    stmt_args = (skill.get_mob_id(), skill.skill_id, skill.total_xp)
    queue_transaction(skill.get_mob_id(), stmt, stmt_args)


def update_mob_skill(skill: MobSkill):
    stmt = update_mob_skills_table
    stmt_args = (skill.total_xp, skill.get_mob_id(), skill.skill_id)
    queue_transaction(skill.get_mob_id(), stmt, stmt_args)


def delete_mob_skills(mob_id: int):
    stmt = delete_mob_skills_table
    stmt_args = (mob_id,)
    queue_transaction(mob_id, stmt, stmt_args)


def init_mob_skill(db_row):
    if db_row:
        return MobSkill(db_row[0], db_row[1], db_row[2])
    else:
        return None
