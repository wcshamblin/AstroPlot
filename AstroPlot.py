#!/usr/bin/python3
import plotly.express as px
import pandas as pd
import argparse
import numpy as np
ps = argparse.ArgumentParser(description='Parses and plots data from JPL\'s HORIZONS system')
ps.add_argument("path", type=str, nargs="+", help='Path to csv to be plotted')
args=ps.parse_args()

cent={'X':0,'Y':0,'Z':0}

cent=pd.DataFrame(np.array([[0,0,0]]),columns=['X', 'Y', 'Z'])

fig=px.scatter_3d(cent, 'X', 'Y', 'Z')
try:
	for csv in args.path:
		orbit=pd.read_csv(csv)
		orbit=orbit.loc[:, ~orbit.columns.str.contains('^Unnamed')]
		orbit.rename(columns=lambda i: i.strip(), inplace=True)
		orbit.dropna(inplace=True)
		orbit['TotalSpeed'] = (abs(orbit.VX)+abs(orbit.VY)+abs(orbit.VZ))
		orbit=px.scatter_3d(orbit, 'X', 'Y', 'Z', color='TotalSpeed')
		fig.add_trace(orbit.data[0])
except FileNotFoundError as error:
	print("Error: "+csv+" could not be read as a csv")
	exit()
fig.update_traces(marker=dict(size=1))
fig.show()