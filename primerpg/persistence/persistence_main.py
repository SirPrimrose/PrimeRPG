#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
from primerpg.helpers.checksum_helper import update_checksums
from primerpg.persistence.boss_persistence import populate_bosses_table, create_bosses_query
from primerpg.persistence.command_requirement_persistence import (
    create_command_requirements_query,
    populate_command_requirements_table,
)
from primerpg.persistence.command_usage_persistence import create_command_usages_query
from primerpg.persistence.connection_handler import (
    connection,
    process_queue,
)
from primerpg.persistence.damage_type_persistence import create_damage_types_query, populate_damage_types_table
from primerpg.persistence.equipment_categories_persistence import (
    create_equipment_categories_query,
    populate_equipment_categories_table,
)
from primerpg.persistence.equipment_stat_categories_persistence import (
    create_equipment_stat_categories_query,
    populate_equipment_stat_categories_table,
)
from primerpg.persistence.equipment_stat_persistence import (
    create_equipment_stats_query,
    populate_equipment_stats_table,
)
from primerpg.persistence.file_checksum_persistence import create_file_checksums_query
from primerpg.persistence.fish_persistence import create_fish_query, populate_fish_table
from primerpg.persistence.inventory_persistence import create_inventory_query
from primerpg.persistence.item_categories_persistence import (
    populate_item_categories_table,
    create_item_categories_query,
)
from primerpg.persistence.items_persistence import (
    create_items_query,
    populate_items_table,
)
from primerpg.persistence.mob_drop_persistence import (
    populate_mob_drops_table,
    create_mob_drops_query,
)
from primerpg.persistence.mob_equipment_persistence import create_mob_equipment_query, populate_mob_equipment_table
from primerpg.persistence.mob_persistence import create_mobs_query, populate_mobs_table
from primerpg.persistence.mob_skill_persistence import (
    populate_mob_skills_table,
    create_mob_skills_query,
)
from primerpg.persistence.move_persistence import (
    create_moves_query,
    populate_moves_table,
)
from primerpg.persistence.moveset_persistence import (
    create_movesets_query,
    populate_movesets_table,
)
from primerpg.persistence.player_equipment_persistence import create_player_equipment_query
from primerpg.persistence.player_persistence import create_players_query
from primerpg.persistence.player_rank_persistence import create_player_ranks_query
from primerpg.persistence.player_skill_persistence import create_player_skills_query
from primerpg.persistence.player_state_persistence import create_player_states_query, populate_player_states_table
from primerpg.persistence.player_task_persistence import create_player_tasks_query
from primerpg.persistence.skill_category_persistence import (
    create_skill_categories_query,
    populate_skill_categories_table,
)
from primerpg.persistence.task_category_persistence import (
    create_task_categories_query,
    populate_task_categories_table,
)
from primerpg.persistence.zone_persistence import create_zones_query, populate_zones_table


def setup_db():
    create_tables()


def save_queue():
    process_queue()


def create_tables():
    cursor_obj = connection.cursor()

    # Utility tables
    cursor_obj.execute(create_file_checksums_query)

    # Raw data tables
    cursor_obj.execute(create_zones_query)
    cursor_obj.execute(create_player_states_query)
    cursor_obj.execute(create_command_requirements_query)
    cursor_obj.execute(create_items_query)
    cursor_obj.execute(create_fish_query)
    cursor_obj.execute(create_item_categories_query)
    cursor_obj.execute(create_equipment_categories_query)
    cursor_obj.execute(create_skill_categories_query)
    cursor_obj.execute(create_equipment_stat_categories_query)
    cursor_obj.execute(create_equipment_stats_query)
    cursor_obj.execute(create_task_categories_query)
    cursor_obj.execute(create_mobs_query)
    cursor_obj.execute(create_mob_skills_query)
    cursor_obj.execute(create_mob_equipment_query)
    cursor_obj.execute(create_mob_drops_query)
    cursor_obj.execute(create_damage_types_query)
    cursor_obj.execute(create_moves_query)
    cursor_obj.execute(create_movesets_query)
    cursor_obj.execute(create_bosses_query)

    # Mutable tables
    cursor_obj.execute(create_command_usages_query)
    cursor_obj.execute(create_players_query)
    cursor_obj.execute(create_player_tasks_query)
    cursor_obj.execute(create_player_skills_query)
    cursor_obj.execute(create_player_equipment_query)
    cursor_obj.execute(create_inventory_query)
    cursor_obj.execute(create_player_ranks_query)

    # Populate raw data tables
    populate_zones_table()
    populate_player_states_table()
    populate_command_requirements_table()
    populate_items_table()
    populate_fish_table()
    populate_item_categories_table()
    populate_skill_categories_table()
    populate_equipment_categories_table()
    populate_equipment_stat_categories_table()
    populate_equipment_stats_table()
    populate_task_categories_table()
    populate_mobs_table()
    populate_mob_skills_table()
    populate_mob_equipment_table()
    populate_mob_drops_table()
    populate_damage_types_table()
    populate_moves_table()
    populate_movesets_table()
    populate_bosses_table()

    update_checksums()

    connection.commit()
