# -*- coding:utf-8 -*-
"""
Script to query external data for the Matisse tool


Usage :

python matisseExternalData.py

Matisse query for external catalog


optional arguments:
  -h, --help            show this help message and exit
  --c1min C1MIN         Min Longitude (in degrees by default)
  --c1max C1MAX         Max Longitude (in degrees by default)
  --c2min C2MIN         Min Latitude (in degrees by default)
  --c2max C2MAX         Max Latitude (in degrees by default)
  --Time_min TIME_MIN   Acquisition start time - format YYYY-MM-DDTHH:MM:SS.m
  --Time_max TIME_MAX   Acquisition stop time - format YYYY-MM-DDTHH:MM:SS.m
  --Incidence_min INCIDENCE_MIN
                        Min incidence angle (solar zenithal angle)
  --Incidence_max INCIDENCE_MAX
                        Max incidence angle (solar zenithal angle)
  --Emerge_min EMERGE_MIN
                        Min emerge angle
  --Emerge_max EMERGE_MAX
                        Max emerge angle
  --Phase_min PHASE_MIN
                        Min phase angle
  --Phase_max PHASE_MAX
                        Max phase angle
  --log LOG             log file, default stdout
  --verbose VERBOSE     verbose mode, default json

required  arguments:
  --target {mercury,moon}
                        target to query
  --ihid IHID           instrument host ID
  --iid IID             instrument ID

"""




SCRIPT_CONFIG = {'moon': 'MatisseNASA/matisseRestNASAMoon.py',
                 'mercury': 'MatisseNASA/matisseRestNASAMercury.py'}


import argparse
import subprocess

def nice_print(string_toprint):
    if string_toprint: print string_toprint

def main(parser):

    args = parser.parse_args()

    script_to_call = SCRIPT_CONFIG.get(args.target.lower(), '')

    switch = ' '.join(['--%s %s' % (item, value) for item, value in args.__dict__.iteritems()
                        if value and item != 'target'])

    cmd = "python %s %s " % (script_to_call, switch)

    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()

    nice_print(out)
    nice_print(err)
    nice_print(process.returncode)


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
                        help="Min Longitude  (in degrees by default)")
    parser.add_argument('--c1max',
                        help="Max Longitude (in degrees by default)")
    parser.add_argument('--c2min',
                        help="Min Latitude (in degrees by default) ")
    parser.add_argument('--c2max',
                        help="Max Latitude(in degrees by default) ")

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
