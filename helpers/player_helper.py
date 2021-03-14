import consts
from data.entity_base import EntityBase
from persistence.dto.player_core import PlayerCore, idle_state
from data.player_profile import PlayerProfile
from persistence.dto.player_skill import PlayerSkill
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
from util import req_xp_for_level, calculate_max_hp, xp_at_level

starting_vitality_level = 5

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

level_loss_on_death = 0.5  # percent
level_min_for_loss = 5  # level number


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


def save_player_profile(player_profile: PlayerProfile) -> None:
    update_player_data(player_profile.core)
    for skill in player_profile.skills:
        update_player_skill(skill)
    for equipment in player_profile.equipment:
        update_player_equipment(equipment)


def heal_player_profile(player_profile: PlayerProfile, hp_to_heal: int = None) -> None:
    if hp_to_heal is None:
        player_profile.set_current_hp(player_profile.get_max_hp())
    else:
        player_profile.change_current_hp(hp_to_heal)


def apply_death_penalty(player_profile: EntityBase) -> None:
    """Applies a penalty for a player's death.

    - Reduces skill xp (50% per skill) for skills above level 5

    :param player_profile: The profile to alter
    """
    for skill in player_profile.skills:
        if skill.get_level() < level_min_for_loss:
            continue
        level_loss = min(skill.progress_to_next_level(), level_loss_on_death)
        prev_level_loss = level_loss_on_death - level_loss
        xp_loss = level_loss * xp_at_level(
            skill.get_level() + 1
        ) + prev_level_loss * xp_at_level(skill.get_level())
        skill.modify_xp(-xp_loss)

        if skill.get_level() < level_min_for_loss:
            skill.set_level(level_min_for_loss)
        # Special condition: Make sure Vit skill does not go below starting level
        if skill.skill_id == consts.vitality_skill_id:
            if skill.get_level() < starting_vitality_level:
                skill.set_level(starting_vitality_level)
