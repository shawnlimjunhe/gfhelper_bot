import datetime as dt
import common
import pytz

PYTZ_SGT = "Asia/Singapore"


def get_datetime_utc_now():
    """
    Creates and returns an 'aware' datetime object in UTC
    """
    return pytz.utc.localize(dt.datetime.utcnow())


def get_datetime_sgt_now():
    """
    Creates and returns an 'aware' datetime object in SGT
    """
    sg_timezone = pytz.timezone(PYTZ_SGT)
    d_naive = dt.datetime.now()
    return sg_timezone.localize(d_naive)


def convert_utc_to_sgt(date: dt.datetime) -> dt.datetime:
    return date.astimezone(pytz.timezone(PYTZ_SGT))


def convert_sgt_to_utc(date: dt.datetime) -> dt.datetime:
    return date.astimezone(pytz.timezone("Etc/UTC"))


def process_hhmm_time(txt: str) -> dt.time:
    """
    process the HH:MM period format in SGT and 
    creates an 'aware' datetime object in UTC 

    """

    txt = txt.replace(" ", "")
    # position of hour depends on whether input is in the form
    # HHMMp or HMMp
    raw_hour = int(txt[:2]) if len(txt) == 5 else int(txt[:1])
    minute = int(txt[-3:-1])
    period = txt[-1]

    hour = int(raw_hour)
    if period == 'p' and hour != 12:
        hour += 12

    if period == 'a' and hour == 12:
        # handle 1200a
        hour = 0

    if hour > 23:
        raise ValueError('hours cannot be more than 23')
    if minute > 59:
        raise ValueError('minutes cannot be more than 59')

    sgt_now = get_datetime_sgt_now()
    utc_now = get_datetime_utc_now()

    sgt_processed_dt = sgt_now.replace(hour=int(hour), minute=minute)
    utc_process_dt = convert_sgt_to_utc(sgt_processed_dt)

    if utc_process_dt < utc_now:
        utc_process_dt += dt.timedelta(days=1)

    return utc_process_dt


def process_h_or_m_time(txt: str) -> dt.timedelta:
    """
    process the h or m time format, e.g. 10 m or 1 h
    and returns a timedelta if successful

    otherwise raises a ValueError if input is invalid
    """
    if txt[-1] == 'h':
        # hours
        hours = int(txt[:-1].strip())
        if hours > 23:
            raise ValueError('hours cannot be more than 23')
        if hours == 0:
            raise ValueError('hours cannot be 0')

        return dt.timedelta(hours=-hours)

    else:
        # minutes
        minutes = int(txt[:-1].strip())
        if minutes == 0:
            raise ValueError('minutes cannot be 0')

        return dt.timedelta(minutes=-minutes)


def process_hm_time(txt: str):
    """
    process the hm time format, e.g. 1h 10m
    and returns a timedelta if successful

    otherwise raises a ValueError if input is invalid
    """
    hours = int(txt.split('h')[0])
    minutes_str = txt.split()[1]
    if 'm' in minutes_str:
        minutes_str = minutes_str[:-1]

    minutes = int(minutes_str)

    if minutes > 59:
        raise ValueError('minutes cannot be more than 59')

    if hours > 23:
        raise ValueError('hours cannot be more than 23')

    if minutes == 0 and hours == 0:
        raise ValueError('hours and minutes cannot both be 0')

    return dt.timedelta(hours=-hours, minutes=-minutes)


def underline_str(text: str) -> str:
    """Returns a string that would be underlined formatted as underlined in MARKDOWN V2"""
    if not text:
        return text
    return ("__" + text + "__")


def time_input_err_to_str(err_msg: str) -> str:
    return (
        common.hedgehog +
        'Sorry the time you send was invalid as:\n' +
        f'{err_msg}\n' +
        'please try again!'
    )
