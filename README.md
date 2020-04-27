# AstroPlot.py
AstroPlot plots the result of JPL's [HORIZONS System](https://ssd.jpl.nasa.gov/?horizons)

## Collecting ephemeris:
Ensure that Vectors mode is selected

Table output should be in CSV format with Corrections at None

Tables should start with the line of columns (X, Y, Z), and end with $$EOE

## Running:
```bash
chmod 755 ./AstroPlot.py
./AstroPlot.py /path/to/csv
```

Keep in mind all CSV's must have the same properties (center, units, etc...) to be plotted together, otherwise they will not make any sense when compared.

## Planned features
* Automatic on-the-fly unit conversion
* Close encounters
* Automatic querying of the HORIZONS system (No planned date, as the system will soon undergo changes with the API, rendering any current code unapplicable)
* Animation (When plotly supports *effecient* 3D animations)
* Automatic re-centering
