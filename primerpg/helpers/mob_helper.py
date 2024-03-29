#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import random
from typing import List

from primerpg.data.item_amount import ItemAmount
from primerpg.data.mob_profile import MobProfile
from primerpg.persistence.mob_drop_persistence import get_all_mob_drops
from primerpg.persistence.mob_equipment_persistence import get_all_mob_equipment
from primerpg.persistence.mob_persistence import get_mob
from primerpg.persistence.mob_skill_persistence import get_all_mob_skills
from primerpg.util import roll_gaussian_dist_for_drop


def get_mob_profile(mob_id: int) -> MobProfile:
    core = get_mob(mob_id)
    skills = get_all_mob_skills(mob_id)
    equipment = get_all_mob_equipment(mob_id)
    drops = get_all_mob_drops(mob_id)
    return MobProfile(core, skills, equipment, drops)


def get_mob_kill_rewards(mob_profile: MobProfile) -> List[ItemAmount]:
    """Rolls the drop table for a mob. All drops are independently rolled and amounts are determined by a mean and
    std deviation.

    :param mob_profile: The mob to drop items for
    :return: The drop dictionary of item ids to item amounts
    """
    rewards: List[ItemAmount] = []
    for drop in mob_profile.drops:
        if random.random() < drop.drop_rate:
            drop_amount = int(roll_gaussian_dist_for_drop(drop.mean, drop.std_dev))
            rewards.append(ItemAmount(drop.item_id, drop_amount))
    return rewards
