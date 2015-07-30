#MatisseRestNasa

External scripts to perform data retrieval for the **Matisse SSE visualization
tool** (https://tools.asdc.asi.it/matisse.jsp)

The main script is **matisseExternalData.py**

```
python matisseExternalData.py

Matisse query for external catalog

optional arguments:
  -h, --help            show this help message and exit
  --c1min C1MIN         Min of first coordinate (in degrees by default)
  --c1max C1MAX         Max of first coordinate (in degrees by default)
  --c2min C2MIN         Min of second coordinate (in degrees by default)
  --c2max C2MAX         Max of second coordinate (in degrees by default)
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

```

The script will go to query different scripts, depending of the target choose.

##MatisseNASA:

Queries to the Orbital Data Explorer (ODE) Rest Interface (NASA Planetary Data System)

Active target: moon, mercury

For the target moon, **matisseRestNASAMoon.py** is used.
Available ihid : 'CH1-ORB', 'CLEM', 'LRO'

For the target Mercury,  **matisseRestNASAMercury.py** is used.
Available ihid: 'messenger'

The scripts can be called from the main script, that will forward to the right script,
or directly.

##MatisseVO:

Queries to the Vespa , Virtual European Solar and Planetary Access
 (http://voparis-europlanet.obspm.fr/EPN2020.html)

 TODO: implement
