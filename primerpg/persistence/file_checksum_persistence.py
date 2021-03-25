#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

from typing import List

from primerpg.persistence.connection_handler import connection
from primerpg.persistence.dto.file_checksum import FileChecksum
from primerpg.persistence.persistence_exception import PersistenceException

file_checksums_table = "file_checksums"

select_file_checksum_query = "SELECT * FROM %s WHERE file_name = ?" % file_checksums_table
select_all_file_checksums_query = "SELECT * FROM %s" % file_checksums_table
create_file_checksums_query = (
    "CREATE TABLE IF NOT EXISTS %s ("
    "file_name text PRIMARY KEY, "
    "md5_checksum text NOT NULL)" % file_checksums_table
)
update_file_checksum_query = "UPDATE %s SET md5_checksum = ? WHERE file_name = ?" % file_checksums_table
insert_file_checksum_query = "INSERT INTO %s (file_name, md5_checksum) VALUES (?, ?)" % file_checksums_table


def get_file_checksum(file_name: str) -> FileChecksum:
    cursor_obj = connection.cursor()

    stmt_args = (file_name,)
    statement = select_file_checksum_query
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return init_file_checksum(result)


def get_all_file_checksums() -> list[FileChecksum]:
    cursor_obj = connection.cursor()

    statement = select_all_file_checksums_query
    cursor_obj.execute(statement)
    result = cursor_obj.fetchall()

    return [init_file_checksum(r) for r in result]


def insert_file_checksum(checksum: FileChecksum) -> None:
    cursor_obj = connection.cursor()

    stmt = insert_file_checksum_query
    stmt_args = (checksum.file_name, checksum.md5_checksum)
    cursor_obj.execute(stmt, stmt_args)


def update_file_checksum(checksum: FileChecksum) -> None:
    cursor_obj = connection.cursor()

    stmt = update_file_checksum_query
    stmt_args = (checksum.md5_checksum, checksum.file_name)
    cursor_obj.execute(stmt, stmt_args)


def init_file_checksum(db_row) -> FileChecksum:
    if db_row:
        return FileChecksum(
            db_row[0],
            db_row[1],
        )
    else:
        raise PersistenceException(FileChecksum)
