from data.player_core import idle_state, default_start_hp
from data.player_profile import PlayerProfile
from data.player_skill import PlayerSkill
from persistence.player_equipment_persistence import get_all_player_equipment
from persistence.player_persistence import insert_player_data, get_player
from persistence.player_skill_persistence import (
    get_all_player_skills,
    insert_player_skill,
)
from persistence.skill_categories_persistence import get_all_skill_categories


def create_new_player_data(player_id, player_name):
    insert_player_data(player_id, player_name, idle_state, default_start_hp)
    for skill in get_all_skill_categories():
        insert_player_skill(PlayerSkill(player_id, skill.unique_id, 0))


def get_player_profile(player_id) -> PlayerProfile:
    core = get_player(player_id)
    skills = get_all_player_skills(player_id)
    equipment = get_all_player_equipment(player_id)
    return PlayerProfile(core, skills, equipment)
