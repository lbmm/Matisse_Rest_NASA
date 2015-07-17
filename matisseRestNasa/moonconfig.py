"""
This the configuration file for The Moon data retrival
List all the accepted IHID and all the IID
define for each which files are the imagine files and the
geometry files, and for each mission what pt use.
Defines if there are conditions for the files to satisfy
"""

# MOON IHID that script accepts
ihid = ['CH1-ORB', 'CLEM', 'LRO']

#Moon iIID (Instrument) that the script accepts
iid = ['M3', 'HIRES', 'LROC']


configurations = {'CH1-ORB': {'M3':
                                  {'pt': 'CALIV3'}},
                  'CLEM': {'HIRES':
                               {'pt': 'EDR'}},
                  'LRO': {'LROC':
                              {'pt': 'CDRNAC'}}}

