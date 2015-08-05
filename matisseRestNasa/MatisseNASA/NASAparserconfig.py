"""
This the
"""
import argparse

from utilities import valid_date, str2bool

def argumentParser(description=''):

    """
    set a command line parser common for the NASAqueries.

    :param description:
    :return: parser
    """

    parser = argparse.ArgumentParser(description=description)
    # Define the command line options

    #coordinates (c1, c2, c3)
    parser.add_argument('--c1min', dest='westernlon', type=float,
                        help="Min Longitude  (in degrees by default)")
    parser.add_argument('--c1max', dest='easternlon', type=float,
                        help="Max Longitude (in degrees by default)")
    parser.add_argument('--c2min', type=float, dest='minlat',
                        help="Min Latitude (in degrees by default) ")
    parser.add_argument('--c2max', type=float, dest='maxlat',
                        help="Max Latitude(in degrees by default) ")

    #times
    parser.add_argument('--Time_min', dest='minobtime', type=valid_date,
                        help="Acquisition start time - format YYYY-MM-DDTHH:MM:SS.m")
    parser.add_argument('--Time_max', dest='maxobtime', type=valid_date,
                        help="Acquisition stop time - format YYYY-MM-DDTHH:MM:SS.m")
    #angles

    parser.add_argument('--Incidence_min', dest='mininangle', type=float,
                        help="Min incidence angle (solar zenithal angle)")

    parser.add_argument('--Incidence_max', dest='maxinangle', type=float,
                        help="Max incidence angle (solar zenithal angle)")

    parser.add_argument('--Emerge_min', dest='minemangle', type=float,
                        help="Min emerge angle")

    parser.add_argument('--Emerge_max', dest='maxemangle', type=float,
                        help="Max emerge angle")

    parser.add_argument('--Phase_min', dest='minphangle', type=float,
                        help="Min phase angle")

    parser.add_argument('--Phase_max', dest='maxpjangle', type=float,
                        help="Max phase angle")

    parser.add_argument('--log', dest='log',
                        help="log file, default stdout")

    parser.register('type', 'bool', str2bool)

    parser.add_argument('--verbose', dest='verbose', type='bool',
                        help="verbose mode, default json")

    return parser


"""
Configuration options for The Moon data retrieval
List all the accepted IHID and all the IID
define for each which files are the imagine files and the
geometry files, and for each mission what pt use.
Defines if there are conditions for the files to satisfy
"""


# MOON IHID that script accepts
ihid_moon = ['CH1-ORB', 'CLEM', 'LRO']

#Moon iIID (Instrument) that the script accepts
iid_moon = ['M3', 'HIRES', 'LROC']


configurations = {'CH1-ORB': {'M3':
                                  {'pt': 'CALIV3'}},
                  'CLEM': {'HIRES':
                               {'pt': 'EDR'}},
                  'LRO': {'LROC':
                              {'pt': 'CDRNAC'}}}

"""
Configuration options for The Mercury data retrieval
List all the accepted IHID and all the IID
"""

# Mercury IHID that script accepts
ihid_mercury = ['messenger']

#Moon iIID (Instrument) that the script accepts
iid_mercury = ['mdis-nac']


