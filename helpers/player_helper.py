import consts
from data.player_profile import PlayerProfile
from data.player_skill import PlayerSkill
from persistence.player_equipment_persistence import get_all_player_equipment
from persistence.player_persistence import insert_player_data, get_player
from persistence.player_skill_persistence import (
    get_all_player_skills,
    insert_player_skill,
)
from persistence.skill_categories_persistence import get_all_skill_categories
from util import req_xp_for_level

player_starting_stat = {
    consts.health_skill_id: req_xp_for_level(10),
    consts.strength_skill_id: 0,
    consts.dexterity_skill_id: 0,
    consts.defense_skill_id: 0,
    consts.intellect_skill_id: 0,
    consts.faith_skill_id: 0,
    consts.resistance_skill_id: 0,
    consts.speed_skill_id: 0,
    consts.luck_skill_id: 0,
}


def create_new_player_data(player_id, player_name, avatar_url):
    insert_player_data(player_id, player_name, avatar_url)
    for skill in get_all_skill_categories():
        insert_player_skill(
            PlayerSkill(
                player_id, skill.unique_id, player_starting_stat[skill.unique_id]
            )
        )


def get_player_profile(player_id) -> PlayerProfile:
    core = get_player(player_id)
    skills = get_all_player_skills(player_id)
    equipment = get_all_player_equipment(player_id)
    return PlayerProfile(core, skills, equipment)
