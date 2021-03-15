import datetime


def str_from_date(date):
    return date.isoformat()


def date_from_str(s):
    return datetime.datetime.fromisoformat(s)
