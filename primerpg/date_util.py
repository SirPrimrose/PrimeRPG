#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm

import datetime


def str_from_date(date: datetime):
    return date.isoformat()


def date_from_str(s: str):
    return datetime.datetime.fromisoformat(s)
