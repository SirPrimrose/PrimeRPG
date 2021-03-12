import consts
from persistence.player_persistence import update_player_data, get_all_players
from persistence.player_skill_persistence import get_player_skill
from util import calculate_max_hp


def regen_tick():
    for p in get_all_players():
        vitality = get_player_skill(p.unique_id, consts.vitality_skill_id).level
        p.current_hp = min(
            p.current_hp + p.hp_regen,
            calculate_max_hp(vitality),
        )
        update_player_data(p)
