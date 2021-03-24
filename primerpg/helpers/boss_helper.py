#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from primerpg.data.boss_profile import BossProfile
from primerpg.persistence.boss_persistence import get_boss
from primerpg.persistence.mob_drop_persistence import get_all_mob_drops
from primerpg.persistence.mob_equipment_persistence import get_all_mob_equipment
from primerpg.persistence.mob_skill_persistence import get_all_mob_skills


def get_boss_profile(boss_mob_id: int) -> BossProfile:
    core = get_boss(boss_mob_id)
    skills = get_all_mob_skills(core.mob_id)
    equipment = get_all_mob_equipment(core.mob_id)
    drops = get_all_mob_drops(core.mob_id)
    return BossProfile(core, skills, equipment, drops)
