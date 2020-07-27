from datetime import datetime
from protos.when_pb2 import When


def to_when(date_time):
    """
    :param date_time: A python datetime.
    :return: A When proto or None if the input is not valid.
    """
    try:
        when = When()
        if date_time.hour != 0 or date_time.minute != 0:
            when.time_specified = True
            when.datetime = date_time.isoformat()
        else:
            when.datetime = date_time.date().isoformat()
        return when
    except:
        return None


def to_datetime(when, fallback_timezone):
    """
    :param when: The when input.
    :param fallback_timezone: The timezone to set if not found.
    Should only be used for When's with no time specified.
    :return: A When proto or None if the input is not valid.
    """
    try:
        date_time = datetime.fromisoformat(when.datetime)
        if not date_time.tzinfo:
            date_time = date_time.replace(tzinfo=fallback_timezone)
        return date_time
    except:
        return None
