#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import datetime

hms_format = "{:02}:{:02}:{:02}"


def str_from_date(date: datetime):
    return date.isoformat()


def date_from_str(s: str):
    return datetime.datetime.fromisoformat(s)


def time_since(start_time: datetime) -> datetime.timedelta:
    end_time = datetime.datetime.utcnow()
    return end_time - start_time


def time_delta_to_readable_str(time_d: datetime.timedelta) -> str:
    hours, remainder = divmod(time_d.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_str = ""
    if hours > 0:
        time_str += "{}h".format(hours)
    if minutes > 0:
        if time_str:
            time_str += " "
        time_str += "{}m".format(minutes)
    if seconds > 0 or not time_str:
        if time_str:
            time_str += " "
        time_str += "{}s".format(seconds)
    return time_str


def time_delta_to_str(time_d: datetime.timedelta, format_str: str = hms_format) -> str:
    hours, remainder = divmod(time_d.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return format_str.format(int(hours), int(minutes), int(seconds))
