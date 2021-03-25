#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.player_rank import PlayerRank

player_ranks_table = "player_ranks"

select_player_ranks_query = "SELECT * FROM %s WHERE player_id = ? AND skill_id = ?" % player_ranks_table
select_all_player_ranks_query = "SELECT * FROM %s WHERE player_id = ?" % player_ranks_table
create_player_ranks_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "player_id integer NOT NULL, "
    "skill_id integer NOT NULL, "
    "rank integer NOT NULL, "
    "PRIMARY KEY(player_id, skill_id), "
    "FOREIGN KEY(player_id) REFERENCES players(unique_id))" % player_ranks_table
)
update_player_skill_ranks_query = (
    "INSERT INTO %s SELECT "
    "player_id, skill_id, RANK() OVER (PARTITION BY skill_id ORDER BY total_xp DESC) player_rank "
    "FROM player_skills" % player_ranks_table
)
update_player_total_ranks_query = (
    "INSERT INTO %s SELECT "
    "player_id, 0 skill_id, RANK() OVER(ORDER BY SUM(total_xp) DESC) player_rank "
    "FROM player_skills GROUP BY player_id" % player_ranks_table
)
delete_player_ranks_query = "DELETE from %s" % player_ranks_table


def generate_player_ranks():
    cursor_obj = connection.cursor()

    # Remove previous ranks
    stmt = delete_player_ranks_query
    cursor_obj.execute(stmt)

    # Update ranks with skills table
    stmt = update_player_skill_ranks_query
    cursor_obj.execute(stmt)
    stmt = update_player_total_ranks_query
    cursor_obj.execute(stmt)

    connection.commit()


def get_player_rank(player_id: int, skill_id: int) -> PlayerRank:
    cursor_obj = connection.cursor()

    stmt_args = (
        player_id,
        skill_id,
    )
    statement = select_player_ranks_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_player_rank(result)


def get_all_player_ranks(player_id: int) -> list[PlayerRank]:
    cursor_obj = connection.cursor()

    stmt_args = (player_id,)
    statement = select_all_player_ranks_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchall()

    items = [init_player_rank(x) for x in result]

    return items


def init_player_rank(db_row):
    if db_row:
        return PlayerRank(db_row[0], db_row[1], db_row[2])
    else:
        return None
