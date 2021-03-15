import logging
import sqlite3
import time

from collections import deque
from typing import Optional, Type, List

transaction_queue = deque()
spam_list: List[int] = []

# Global Var for database connection
connection = sqlite3.connect("primeRPG.db")
# Foreign keys boost performance for selects, but degrade performance for insert, delete, and updates
# Therefore, use foreign keys in tables that will be read, but not written to (Equipment Stats, Fish, etc.)
# https://www.experts-exchange.com/articles/4293/Can-Foreign-key-improve-performance.html
connection.execute("PRAGMA foreign_keys = 1")
db_logger = logging.getLogger("db")
connection.set_trace_callback(db_logger.info)


def queue_transaction(player_id: Optional[int], sql, params):
    transaction_queue.append({"sql": sql, "params": params})
    if player_id:
        spam_list.append(player_id)


def process_queue():
    if len(transaction_queue) == 0:
        return
    print("{0} transactions to run...".format(len(transaction_queue)))
    t = time.time()
    cursor_obj = connection.cursor()
    cursor_obj.execute("BEGIN TRANSACTION")

    while len(transaction_queue) > 0:
        transaction = transaction_queue.popleft()
        safe_execute(cursor_obj, transaction["sql"], transaction["params"])

    connection.commit()
    spam_list.clear()

    print("Time taken: %.3f sec" % (time.time() - t))


def safe_execute(cursor: sqlite3.Cursor, sql, params):
    try:
        cursor.execute(sql, params)
    except (sqlite3.ProgrammingError, sqlite3.IntegrityError) as e:
        print("Exception: {}".format(e))
        print("Error saving\nSQL: {}\nParams: {}".format(sql, params))
