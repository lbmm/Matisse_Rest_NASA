# -*- coding:utf-8 -*-


SCRIPT_CONFIG = {'moon': 'MatisseNASA/matisseRestNASAMoon.py',
                 'mercury': 'MatisseNASA/matisseRestNASAMercury'}


import argparse
import os

def main(parser):

    args = parser.parse_args()

    script_to_call = SCRIPT_CONFIG[args.target.lower()]

    cmd = "python %s " % script_to_call
    stdin, stdout, stderr = os.popen3(cmd)
    stdin.close()
    errmsg = stderr.readlines()
    outmsg = stdout.readlines()
    print errmsg
    print outmsg
    stdout.close()
    stderr.close()






if __name__ == "__main__":



    parser = argparse.ArgumentParser(description="Matisse query for external catalog")
    # Define the command line options


    #type check is demanded to the specifics scripts

    requiredNamed = parser.add_argument_group('required  arguments')

    requiredNamed.add_argument('--target', help="target to query", choices=SCRIPT_CONFIG.keys(),
                               required=True)

    requiredNamed.add_argument('--ihid',  help="instrument host ID",
                               required=True)
    requiredNamed.add_argument('--iid', help="instrument  ID",
                               required=True)

    #coordinates (c1, c2, c3)
    parser.add_argument('--c1min',
                        help="Min of first coordinate (in degrees by default)")
    parser.add_argument('--c1max',
                        help="Max of first coordinate (in degrees by default)")
    parser.add_argument('--c2min',
                        help="Min of second coordinate (in degrees by default) ")
    parser.add_argument('--c2max',
                        help="Max of second coordinate (in degrees by default) ")

    #times
    parser.add_argument('--Time_min',
                        help="Acquisition start time - format YYYY-MM-DDTHH:MM:SS.m")
    parser.add_argument('--Time_max',
                        help="Acquisition stop time - format YYYY-MM-DDTHH:MM:SS.m")
    #angles

    parser.add_argument('--Incidence_min',
                        help="Min incidence angle (solar zenithal angle)")

    parser.add_argument('--Incidence_max',
                        help="Max incidence angle (solar zenithal angle)")

    parser.add_argument('--Emerge_min',
                        help="Min emerge angle")

    parser.add_argument('--Emerge_max',
                        help="Max emerge angle")

    parser.add_argument('--Phase_min',
                        help="Min phase angle")

    parser.add_argument('--Phase_max',
                        help="Max phase angle")

    parser.add_argument('--log',
                        help="log file, default stdout")

    parser.add_argument('--verbose',
                        help="verbose mode, default json")


    main(parser)
