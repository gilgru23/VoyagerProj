from datetime import datetime

date_str_format = "%Y-%m-%d"
date_time_str_format = "%Y-%m-%d %H:%M:%S"


def date_to_str(date: datetime):
    return date.strftime(date_str_format)


def date_time_to_str(date_time: datetime):
    return date_time.strftime(date_time_str_format)
