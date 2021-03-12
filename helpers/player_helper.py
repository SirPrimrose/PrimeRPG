import consts
from data.mob_profile import MobProfile
from data.player_core import PlayerCore, idle_state
from data.player_profile import PlayerProfile
from data.player_skill import PlayerSkill
from persistence.mob_equipment_persistence import get_all_mob_equipment
from persistence.mob_persistence import get_mob
from persistence.mob_skill_persistence import get_all_mob_skills
from persistence.player_equipment_persistence import (
    get_all_player_equipment,
    update_player_equipment,
)
from persistence.player_persistence import (
    insert_player_data,
    get_player,
    update_player_data,
)
from persistence.player_skill_persistence import (
    get_all_player_skills,
    insert_player_skill,
    update_player_skill,
)
from persistence.skill_categories_persistence import get_all_skill_categories
from util import req_xp_for_level, calculate_max_hp

starting_vitality_level = 3

player_starting_skill_xp = {
    consts.vitality_skill_id: req_xp_for_level(starting_vitality_level),
    consts.strength_skill_id: 0,
    consts.dexterity_skill_id: 0,
    consts.defense_skill_id: 0,
    consts.intellect_skill_id: 0,
    consts.faith_skill_id: 0,
    consts.resistance_skill_id: 0,
    consts.speed_skill_id: 0,
    consts.luck_skill_id: 0,
}

player_starting_hp_regen = 0.2


def create_new_player_data(player_id, player_name, avatar_url):
    core = PlayerCore(
        player_id,
        player_name,
        avatar_url,
        idle_state,
        calculate_max_hp(starting_vitality_level),
        player_starting_hp_regen,
    )
    insert_player_data(core)
    for skill in get_all_skill_categories():
        insert_player_skill(
            PlayerSkill(
                player_id, skill.unique_id, player_starting_skill_xp[skill.unique_id]
            )
        )


def get_player_profile(player_id) -> PlayerProfile:
    core = get_player(player_id)
    skills = get_all_player_skills(player_id)
    equipment = get_all_player_equipment(player_id)
    return PlayerProfile(core, skills, equipment)


def save_player_profile(player_profile: PlayerProfile):
    player_profile.core.current_hp = player_profile.current_hp
    update_player_data(player_profile.core)
    for skill in player_profile.skills:
        update_player_skill(skill)
    for equipment in player_profile.equipment:
        update_player_equipment(equipment)


def get_mob_profile(mob_id) -> MobProfile:
    core = get_mob(mob_id)
    skills = get_all_mob_skills(mob_id)
    equipment = get_all_mob_equipment(mob_id)
    return MobProfile(core, core.name, core.icon_url, skills, equipment)
