import datetime as dt
import common
import pytz

PYTZ_SGT = "Asia/Singapore"


def get_datetime_utc_now() -> dt.datetime:
    """Creates and returns an 'aware' datetime object at the current time in UTC"""
    return pytz.utc.localize(dt.datetime.utcnow())


def get_datetime_sgt_now():
    """Creates and returns an 'aware' datetime object in SGT at the current time in SGT"""
    sg_timezone = pytz.timezone(PYTZ_SGT)
    d_naive = dt.datetime.now()
    return sg_timezone.localize(d_naive)


def convert_utc_to_sgt(date: dt.datetime) -> dt.datetime:
    """Converts an 'aware' datetime object from UTC to SGT time"""
    return date.astimezone(pytz.timezone(PYTZ_SGT))


def convert_sgt_to_utc(date: dt.datetime) -> dt.datetime:
    """Converts an 'aware' datetime object from SGT to UTC time"""
    return date.astimezone(pytz.timezone("Etc/UTC"))


def process_hhmm_time(txt: str) -> dt.datetime:
    """
    processes the HH:MM period format in SGT and creates an 'aware' datetime object in UTC 

    Takes in a string matching the regex `^\d{1,}\d{2}\s?[ap]$`
    which is the 'HH:MM a' or 'HH:MMa' (where a is the period) and creates an timezone aware
    datetime object in UTC time. If the time created is before the current time, the created
    datetime object will have a date component 1 day ahead of today. 

    Parameters
    ----------
    txt
        A string following either formats: 'HH:MM p' or 'HH:MMp'


    Returns
    -------
    datetime.datetime
        datetime object

    Raises
    ------
    ValueError
         If the processed hour of `txt` is more than 23 or
         if the MM component of `txt` is more than 59

    Examples
    --------
    >>> process_hhmm_time('10:30p') # SGT time
    datetime(hours=14, minutes=30) # UTC time

    >>> process_hhmm_time('9:00a') # SGT time
    datetime(hours=1, minutes=0) # UTC time

    >>> process_hhmm_time('1:00 a') # SGT time
    datetime(hours=5, minutes=0)
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
    process the h or m time format, e.g. 10 m or 1 h and returns a timedelta object

    Takes in a string matching the regex `^\d{1,3}[hm]$` which is either 'MMm' or either 'HHh'
    and creates the corresponding timedelta object. Adding this timedelta object to a datetime
    object will shift the datetime object's time to an earlier time.    

    Parameters
    ----------
    txt
        A string following the 'MMMm' or 'HHHh' format

    Returns
    -------
    datetime.timedelta
        The timedelta object with -MMM minutes or -HHH hours

    Raises
    ------
    ValueError
        If supplied hours is more than 23 or equals 0, or supplied minutes equals 0

    Examples
        --------
        >>> process_h_or_m_time('1h')
        timedelta(seconds=-3600)

        >>> process_h_or_m_time('999m')
        timedelta(seconds=-59940)

        >>> process_h_or_m_time('24h')
        Traceback (most recent call last):
        ...
        ValueError: 'hours cannot be more than 23'

        >>> process_h_or_m_time('0h')
        Traceback (most recent call last):
        ...
        ValueError: 'hours cannot be 0'
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
        process the hm time format, e.g. 1h 10m and returns a timedelta object

        Takes in a string matching the regex `^\d{1,2}h\s\d{1,2}m$` which is either 'Hh MMm'
        and creates the corresponding timedelta object. Adding this timedelta object to a datetime
        object will shift the datetime object's time to an earlier time.

        Parameters
        ----------
        txt
            A string following the 'Hh MMm' format

        Returns
        -------
        datetime.timedelta
            The timedelta object with -H hours and -MM minutes

        Raises
        ------
        ValueError
            If supplied minutes is more than 59 or supplied hours is more than 59 or both the supplied
            hours and minutes equal 0

        Examples
            --------
            >>> process_hm_time('1h 10m')
            timedelta(seconds=-4200)

            >>> process_hm_time('0h 10m')
            timedelta(seconds=-600)

            >>> process_hm_time('0h 0m')
            Traceback (most recent call last):
            ...
            ValueError: 'hours and minutes cannot both be 0'

            >>> process_hm_time('24h 0m')
            Traceback (most recent call last):
            ...
            ValueError: 'hours cannot be more than 23'

            >>> process_hm_time('0h 60m')
            Traceback (most recent call last):
            ...
            ValueError: 'minutes cannot be more than 59'
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
