import datetime
import logging
from os import mkdir

from consts import log_folder


def setup_logging():
    if not log_folder.exists():
        mkdir(log_folder)
    time = datetime.datetime.utcnow()
    counter = 0
    filename = "db_log_{}_{}.log".format(time.strftime("%d_%m_%y"), counter)
    logfile_path = log_folder / filename
    while logfile_path.exists():
        counter += 1
        filename = "db_log_{}_{}.log".format(time.strftime("%d_%m_%y"), counter)
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
