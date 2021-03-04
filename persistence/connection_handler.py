import sqlite3
import time

from collections import deque

# Open connection to database
connection = sqlite3.connect("primeRPG.db")

t_queue = deque()
spam_list = list()


def queue_transaction(player_id, sql, params):
    t_queue.append({"sql": sql, "params": params})
    spam_list.append(player_id)


def process_queue():
    if len(t_queue) == 0:
        return
    print("{0} transactions to run...".format(len(t_queue)))
    t = time.time()
    cursor_obj = connection.cursor()
    cursor_obj.execute("BEGIN TRANSACTION")

    while len(t_queue) > 0:
        transaction = t_queue.popleft()
        cursor_obj.execute(transaction["sql"], transaction["params"])

    connection.commit()
    spam_list.clear()

    print("Time taken: %.3f sec" % (time.time() - t))
