import consts
from data.entity_base import EntityBase
from data.player_profile import PlayerProfile
from helpers.equipment_helper import equip_player_item
from persistence.dto.player_core import PlayerCore, idle_state
from persistence.dto.player_inventory_item import PlayerInventoryItem
from persistence.dto.player_skill import PlayerSkill
from persistence.inventory_persistence import (
    delete_inventory_items,
    get_all_inventory_items,
    insert_inventory_item,
    update_inventory_item,
    get_inventory_item,
)
from persistence.player_equipment_persistence import (
    get_all_player_equipment,
    update_player_equipment,
    delete_player_equipment,
    insert_player_equipment,
    get_player_equipment,
)
from persistence.player_persistence import (
    insert_player_data,
    get_player,
    update_player_data,
    delete_player_data,
)
from persistence.player_skill_persistence import (
    get_all_player_skills,
    insert_player_skill,
    update_player_skill,
    delete_player_skills,
    get_player_skill,
)
from persistence.skill_categories_persistence import get_all_skill_categories
from persistence.task_persistence import delete_player_tasks
from util import req_xp_for_level, calculate_max_hp, xp_at_level

starting_vitality_level = 5

toy_sword_id = 202
toy_helmet_id = 301

player_starting_hp_regen = 0.2

level_loss_on_death = 0.5  # percent
level_min_for_loss = 5  # level number

player_starting_skill_xp = {
    consts.vitality_skill_id: req_xp_for_level(starting_vitality_level),
}

player_starting_inventory = {toy_sword_id: 1, toy_helmet_id: 1}

player_starting_equipment = [toy_sword_id, toy_helmet_id]


def create_new_player_data(player_id, player_name, avatar_url) -> None:
    core = PlayerCore(
        player_id,
        player_name,
        avatar_url,
        idle_state,
        calculate_max_hp(starting_vitality_level),
        player_starting_hp_regen,
    )
    skills = []
    for skill in get_all_skill_categories():
        xp = 0
        if skill.unique_id in player_starting_skill_xp:
            xp = player_starting_skill_xp[skill.unique_id]
        skills.append(PlayerSkill(player_id, skill.unique_id, xp))
    inventory = []
    for item_id, item_amount in player_starting_inventory.items():
        inventory.append(PlayerInventoryItem(player_id, item_id, item_amount))

    profile = PlayerProfile(core, skills, [], inventory)
    for equip_item_id in player_starting_equipment:
        equip_player_item(profile, equip_item_id)
    insert_player_profile(profile)


def insert_player_profile(player_profile: PlayerProfile) -> None:
    insert_player_data(player_profile.core)
    for skill in player_profile.skills:
        insert_player_skill(skill)
    for equipment in player_profile.equipment:
        insert_player_equipment(equipment)
    for item in player_profile.get_inventory():
        insert_inventory_item(item)


def get_player_profile(player_id) -> PlayerProfile:
    core = get_player(player_id)
    skills = get_all_player_skills(player_id)
    equipment = get_all_player_equipment(player_id)
    inventory = get_all_inventory_items(player_id)
    return PlayerProfile(core, skills, equipment, inventory)


def save_player_profile(player_profile: PlayerProfile) -> None:
    update_player_data(player_profile.core)
    for skill in player_profile.skills:
        if get_player_skill(skill.get_player_id(), skill.skill_id):
            update_player_skill(skill)
        else:
            insert_player_skill(skill)
    for inv_item in player_profile.get_inventory():
        if get_inventory_item(inv_item.player_id, inv_item.item_id):
            update_inventory_item(inv_item)
        else:
            insert_inventory_item(inv_item)

    # TODO Instead of refreshing the entire equip list, only delete/insert differences
    delete_player_equipment(player_profile.core.unique_id)
    for equipment in player_profile.equipment:
        insert_player_equipment(equipment)


def delete_player_profile(player_id: int) -> None:
    delete_player_skills(player_id)
    delete_player_equipment(player_id)
    delete_inventory_items(player_id)
    delete_player_tasks(player_id)
    delete_player_data(player_id)


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
