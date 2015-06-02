from datetime import datetime

def parse_timestamp(timestamp):
    """
        Parse timestamp

        >>> parse_timestamp('2015-4-30 18:59:34')
        datetime.datetime(2015, 4, 30, 18, 59, 34)
    """
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")