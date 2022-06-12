from django.utils import timezone
date_str_format = "%Y-%m-%d"
date_time_str_format = "%Y-%m-%d %H:%M:%S"


def date_to_str(date: timezone):
    return date.strftime(date_str_format)


def date_time_to_str(date_time: timezone):
    return date_time.strftime(date_time_str_format)


def parse_string_to_timezone(date_time_str:str):
    """
    try parse a string to timezone object
    :param date_time_str: string of format "%Y-%m-%d %H:%M:%S"
    :return: if succeeds returns timezone of the given string. else returns timezone.now()
    """
    
    try:
        raw_time = timezone.now().fromisoformat(date_time_str)
        time = timezone.make_aware(raw_time, timezone.get_current_timezone())
    except:
        time = timezone.now()
    return time

