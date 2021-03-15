import datetime
import logging
import os
import time

from consts import log_folder

logfile_date_format = "%y_%m_%d"
days_to_keep_logs = 7


def setup_logging():
    clean_log_folder()
    if not log_folder.exists():
        os.mkdir(log_folder)
    current_time = datetime.datetime.utcnow()
    counter = 0
    filename = "db_log_{}_{}.log".format(
        current_time.strftime(logfile_date_format), counter
    )
    logfile_path = log_folder / filename
    while logfile_path.exists():
        counter += 1
        filename = "db_log_{}_{}.log".format(
            current_time.strftime(logfile_date_format), counter
        )
        logfile_path = log_folder / filename
    init_db_logger(logfile_path)


def init_db_logger(logfile: str):
    log = logging.getLogger("db")
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s:%(message)s")
    fh = logging.FileHandler(logfile, "w")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)


def clean_log_folder():
    now = time.time()

    for f in os.listdir(log_folder):
        f = log_folder / f
        if os.stat(f).st_mtime < now - days_to_keep_logs * 86400:
            if os.path.isfile(f):
                print("Removed old log file: {}".format(f.name))
                os.remove(f)
