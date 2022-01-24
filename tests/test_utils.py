from multiprocessing.sharedctypes import Value
import pytest
import datetime
import utils


@pytest.mark.parametrize(
    "hour, minute, hhmm_string",
    [
        # test hour in UTC time and hhmm_string in SGT
        (1, 30, '930a'),
        (1, 30, '930 a'),
        (1, 30, '0930a'),
        (1, 30, '0930 a'),
        (4, 0, '1200p'),
        (14, 59, '1059p'),
        (16, 0, '1200a'),
        (16, 0, '000a'),
        (4, 0, '000p'),
    ]
)
def test_process_hhmm_time(hour, minute, hhmm_string):
    # setup
    now = utils.get_datetime_utc_now()
    dt = now.replace(hour=hour, minute=minute)

    # test
    test_dt = utils.process_hhmm_time(hhmm_string)

    assert dt.hour == test_dt.hour
    assert dt.minute == test_dt.minute


@pytest.mark.parametrize(
    "hhmm_string, except_msg",
    [
        ('1300p', 'hour cannot be more than 23'),
        ('1260p', 'minutes cannot be more than 59'),
        ('1360a', 'hour cannot be more than 23')
    ]
)
def test_process_hhmm_time_fail(hhmm_string, except_msg):
    with pytest.raises(ValueError) as exc_info:
        utils.process_hhmm_time(hhmm_string)
    assert str(exc_info.value) == except_msg


@pytest.mark.parametrize(
    'hours, minutes, h_or_m_str',
    [
        (-1, None, '1h'),
        (-23, None, '23h'),
        (None, -1, '1m'),
        (None, -999, '999m')
    ]
)
def test_process_h_or_m_time(hours, minutes, h_or_m_str):
    # setup
    if hours:
        timedelta = datetime.timedelta(hours=hours)
    else:
        timedelta = datetime.timedelta(minutes=minutes)

    # testing
    test_timedelta = utils.process_h_or_m_time(h_or_m_str)

    assert timedelta.seconds == test_timedelta.seconds


@pytest.mark.parametrize(
    "h_or_m_str, except_msg",
    [
        ('24h', 'hours cannot be more than 23'),
        ('0h', 'hours cannot be 0'),
        ('0m', 'minutes cannot be 0')
    ]
)
def test_process_hhmm_time_fail(h_or_m_str, except_msg):
    with pytest.raises(ValueError) as exc_info:
        utils.process_h_or_m_time(h_or_m_str)
    assert str(exc_info.value) == except_msg


@pytest.mark.skip(reason="yet to implement")
def test_process_hm_time():
    pass


@pytest.mark.skip(reason="yet to implement")
def test_underline_str():
    pass
