""""
Configuration file for the matisseRestNasa

"""
from collections import OrderedDict

"""
metadata translates fields name from Nasa namespace to
   the  Matisse namespace

"""

metadata = OrderedDict([
    ("startTime", "UTC_start_times"),
    ("stopTime", "UTC_stop_time"),
    ("c2min", "Minimum_latitude"),
    ("c2max", "Maximum_latitude"),
    ("c1min", "Westernmost_longitude"),
    ("c1max", "Easternmost_longitude"),
    ("c3min", 0),
    ("c3max", 0),
    ("incidence_min", "Incidence_angle"),
    ("incidence_max", "Incidence_angle"),
    ("emergence_min", "Emission_angle"),
    ("emergence_max", "Emission_angle"),
    ("phase_min", "Phase_angle"),
    ("phase_max", "Phase_angle")
])

def getMetadata(ihid=None):

    if ihid and ihid == "LRO":
        metadata['Footprint_geometry'] = "Footprint_geometry"

    return metadata
