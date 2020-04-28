# AstroPlot.py
AstroPlot plots the result of JPL's [HORIZONS System](https://ssd.jpl.nasa.gov/?horizons)

## Collecting ephemeris:
Ensure that Vectors mode is selected

Table output should be in CSV format with Corrections at None

Tables should start with the line after login information, and end with $$EOE
```
 Automated mail xmit by PORT_LOGIN, PID= 16019 Tue Apr 28 08:04:43 2020
++++++++++++++++++++++++++++++++ (part 1 of 1)  +++++++++++++++++++++++++++++++
*******************************************************************************
Ephemeris / PORT_LOGIN Tue Apr 28 08:04:37 2020 Pasadena, USA    / Horizons   
******************************************************************************* <-- FILE STARTS HERE
Target body name: Mercury (199)                   {source: DE431mx}
Center body name: Sun (10)                        {source: DE431mx}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2010-Jan-01 00:00:00.0000 TDB
Stop  time      : A.D. 2020-Jan-01 00:00:00.0000 TDB
Step-size       : 1440 minutes
*******************************************************************************
```

## Running:
```bash
chmod 755 ./AstroPlot.py
./AstroPlot.py /path/to/csv
```

Keep in mind all CSV's must have the same properties (center, units, etc...) to be plotted together, otherwise they will not make any sense when compared.

## Planned features
* ~~Automatic on-the-fly unit conversion~~
* Close encounters
* Automatic querying of the HORIZONS system (No planned date, as the system will soon undergo changes with the API, rendering any current code unapplicable)
* Animation (When plotly supports *effecient* 3D animations)
* Automatic re-centering
