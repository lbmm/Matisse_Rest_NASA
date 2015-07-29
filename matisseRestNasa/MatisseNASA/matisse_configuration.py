""""
Configuration file for the matisseRestNasa

"""
from collections import OrderedDict

""" metadata translates fields name from Nasa to
    Matisse"""

metadata = OrderedDict([
    ("start_time", "UTC_start_times"),
    ("stop_time", "UTC_stop_time"),
    ("latitude_min", "Minimum_latitude"),
    ("latitude_max", "Maximum_latitude"),
    ("longitude_min", "Westernmost_longitude"),
    ("longitude_max", "Easternmost_longitude"),
    ("range_to_target_min", 0),
    ("range_to_target_max", 0),
    ("incidence_angle_min", "Incidence_angle"),
    ("incidence_angle_max", "Incidence_angle"),
    ("emergence_angle_min", "Emission_angle"),
    ("emergence_angle_max", "Emission_angle"),
    ("phase_angle_min", "Phase_angle"),
    ("phase_angle_max", "Phase_angle")
])

def getMetadata(ihid=None):

    if ihid and ihid == "LRO":
        metadata['Footprint_geometry'] = "Footprint_geometry"

    return metadata