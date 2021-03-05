import sqlite3
import time

from collections import deque

transaction_queue = deque()
spam_list = list()

# Global Var for database connection
connection = sqlite3.connect("primeRPG.db")
# Foreign keys boost performance for selects, but degrade performance for insert, delete, and updates
# Therefore, use foreign keys in tables that will be read, but not written to (Equipment Stats, Fish, etc.)
# https://www.experts-exchange.com/articles/4293/Can-Foreign-key-improve-performance.html
connection.execute("PRAGMA foreign_keys = 1")


def queue_transaction(player_id, sql, params):
    transaction_queue.append({"sql": sql, "params": params})
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
        cursor_obj.execute(transaction["sql"], transaction["params"])

    connection.commit()
    spam_list.clear()

    print("Time taken: %.3f sec" % (time.time() - t))
