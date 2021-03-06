
from datetime import datetime
import argparse


def valid_date(s):
    """"
    Validation of the command line options.
    Check if a date is of the right format
    e.g. = 2013-01-08T15:39:05.169

    Arg: string
    Return: string
    Raise ArgumentTypeError
    """

    try:
        datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
        #date string is well formatted
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)



def set_default(obj):
    if isinstance(obj, set):
        return dict(obj)
    raise TypeError



