#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg import consts
from primerpg.persistence.player_persistence import update_player_data, get_all_players, update_player_regen_data
from primerpg.persistence.player_skill_persistence import get_player_skill
from primerpg.util import calculate_max_hp


def regen_tick():
    for p in get_all_players():
        vitality = get_player_skill(p.unique_id, consts.vitality_skill_id).get_level()
        new_hp = min(
            p.current_hp + p.hp_regen,
            calculate_max_hp(vitality),
        )
        if p.current_hp != new_hp:
            p.current_hp = new_hp
            update_player_regen_data(p)
