from persistence.connection_handler import (
    connection,
    process_queue,
)
from persistence.equipment_categories_persistence import (
    create_equipment_categories_query,
    populate_equipment_categories_table,
)
from persistence.equipment_stat_categories_persistence import (
    create_equipment_stat_categories_query,
    populate_equipment_stat_categories_table,
)
from persistence.equipment_stat_persistence import (
    create_equipment_stats_query,
    populate_equipment_stats_table,
)
from persistence.fish_persistence import create_fish_query, populate_fish_table
from persistence.inventory_persistence import create_inventory_query
from persistence.item_categories_persistence import (
    populate_item_categories_table,
    create_item_categories_query,
)
from persistence.items_persistence import create_items_query, populate_items_table
from persistence.mob_equipment_persistence import (
    populate_mob_equipment_table,
    create_mob_equipment_query,
)
from persistence.mob_persistence import create_mobs_query, populate_mobs_table
from persistence.mob_skill_persistence import (
    populate_mob_skills_table,
    create_mob_skills_query,
)
from persistence.player_equipment_persistence import create_player_equipment_query
from persistence.player_persistence import create_players_query
from persistence.player_skill_persistence import create_player_skills_query
from persistence.skill_categories_persistence import (
    create_skill_categories_query,
    populate_skill_categories_table,
)
from persistence.task_persistence import create_player_tasks_query


def setup_db():
    create_tables()


def save_queue():
    process_queue()


def create_tables():
    cursor_obj = connection.cursor()

    # Raw data tables
    cursor_obj.execute(create_items_query)
    cursor_obj.execute(create_fish_query)
    cursor_obj.execute(create_item_categories_query)
    cursor_obj.execute(create_equipment_categories_query)
    cursor_obj.execute(create_skill_categories_query)
    cursor_obj.execute(create_equipment_stat_categories_query)
    cursor_obj.execute(create_equipment_stats_query)
    cursor_obj.execute(create_mobs_query)
    cursor_obj.execute(create_mob_skills_query)
    cursor_obj.execute(create_mob_equipment_query)

    # Mutable tables
    cursor_obj.execute(create_players_query)
    cursor_obj.execute(create_player_tasks_query)
    cursor_obj.execute(create_player_skills_query)
    cursor_obj.execute(create_player_equipment_query)
    cursor_obj.execute(create_inventory_query)

    # Populate raw data tables
    populate_items_table()
    populate_fish_table()
    populate_item_categories_table()
    populate_skill_categories_table()
    populate_equipment_categories_table()
    populate_equipment_stat_categories_table()
    populate_equipment_stats_table()
    populate_mobs_table()
    populate_mob_skills_table()
    populate_mob_equipment_table()

    connection.commit()
