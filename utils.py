import time
import datetime


def current_time_ms():
    """
    Get the current time in milliseconds since the epoch.

    Returns:
        int: The current time in milliseconds.
    """
    return int(time.time() * 1000)


def timestamp_to_datetime(timestamp_ms):
    """
    Convert a timestamp in milliseconds to a datetime object.

    Args:
        timestamp_ms (int): The timestamp in milliseconds.

    Returns:
        datetime.datetime: The corresponding datetime object.
    """
    return datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
