#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from primerpg.persistence.player_persistence import get_player, update_player_state_data

idle_state_id = 1
gathering_state_id = 2
recon_state_id = 3

player_states = [idle_state_id, gathering_state_id, recon_state_id]


def set_player_state(player_id: int, state_id: int):
    player_core = get_player(player_id)
    player_core.state_id = state_id
    update_player_state_data(player_core)
