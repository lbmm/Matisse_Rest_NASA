# -*- coding:utf-8 -*-
from collections import namedtuple
import unittest

from matisseRestNASA import count_visitors, Visitor

"""
test dataset
"""

DATASET = "12:57,13:06\n" + "15:26,15:49\n" + "12:07,12:24\n" \
           + "17:11,17:28\n" + "10:28,10:44\n" + "11:24,11:45\n" \
           + "09:52,10:16\n" + "15:15,15:40\n" + "11:16,11:41\n" \
           + "13:49,14:14\n" + "12:25,12:44\n" + "10:21,10:38\n" \
           + "13:20,13:42\n" + "15:41,15:55\n" + "09:47,10:12\n" \
           + "08:14,08:25\n" + "11:09,11:31\n" + "16:40,16:56\n" \
           + "12:13,12:18\n" + "15:41,16:09"

"""
dummy function uses to build a list of Visitor from a string
This is done for testing purpose
"""


def buildDataset(dataset):
    data_aray = dataset.split('\n')

    for record in data_aray:

        data = namedtuple('Data', ['in_time', 'out_time'])
        lines = record.split(',')

        try:
            #sanity check: needs two entries per row
            if len(lines) != 2:
                 raise ValueError
            data_recorded = data(*lines)
            for key in data_recorded._fields:
                yield (Visitor(getattr(data_recorded, key), key))
        except ValueError as e:
                #skipping data in wrong format
                continue

"""
test to check if results are consistent with a dummy dataset
"""


class TestVisitingTimes(unittest.TestCase):

    def test(self):

        result = count_visitors(buildDataset(DATASET))
        self.assertEqual(result['in'].strftime('%H:%M'), '15:41', "in time OK")
        self.assertEqual(result['out'].strftime('%H:%M'),  '15:49', "out time OK")
        self.assertEqual(result['max_visitors'], 3, "max visitor OK")


if __name__ == '__main__':

    unittest.main()


