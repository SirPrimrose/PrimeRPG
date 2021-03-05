from data.player import idle_state, default_start_hp
from persistence.player_persistence import insert_player_data


def create_new_player_data(player_id, player_name):
    insert_player_data(player_id, player_name, idle_state, default_start_hp)
    # Create all player skills in player skills db
