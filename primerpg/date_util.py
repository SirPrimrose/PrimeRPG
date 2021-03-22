#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import datetime


def str_from_date(date: datetime):
    return date.isoformat()


def date_from_str(s: str):
    return datetime.datetime.fromisoformat(s)


def time_since(start_time: datetime) -> datetime.timedelta:
    end_time = datetime.datetime.utcnow()
    return end_time - start_time


def time_delta_to_str(time_d: datetime.timedelta):
    hours, remainder = divmod(time_d.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
