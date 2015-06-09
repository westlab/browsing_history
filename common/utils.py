from datetime import datetime, timedelta
from itertools import tee

def parse_timestamp(timestamp):
    """
        Parse timestamp

        >>> parse_timestamp('2015-4-30 18:59:34')
        datetime.datetime(2015, 4, 30, 18, 59, 34)
    """
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def round_datetime_by_minute(dt):
    rounded_dt = dt - timedelta(minutes=dt.minute % 10,
                                seconds=dt.second,
                                microseconds=dt.microsecond)
    return rounded_dt

def pairwise(iterable):
    """
        s -> (s0, s1), (s1, s2), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
