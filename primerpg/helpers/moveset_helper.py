#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from primerpg.consts import weapon_category_id
from primerpg.data.entity_base import EntityBase
from primerpg.data_cache import get_item_moveset_ids
from primerpg.persistence.moveset_persistence import get_moveset


def get_all_move_ids(profile: EntityBase):
    moveset_ids = get_item_moveset_ids(profile.get_equipment(weapon_category_id).item_id)
    move_ids = []
    for moveset_id in moveset_ids:
        move_ids += get_moveset(moveset_id).move_ids
    return move_ids
