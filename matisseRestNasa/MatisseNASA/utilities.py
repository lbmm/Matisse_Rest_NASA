"""
Utility module for the package MatisseNASA
"""


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


def str2bool(v):
  #susendberg's function
  return v.lower() in ("yes", "true", "t", "1")



