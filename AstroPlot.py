#!/usr/bin/python3
import plotly.graph_objects as go
import pandas as pd
import argparse
import numpy as np
ps = argparse.ArgumentParser(description='Parses and plots data from JPL\'s HORIZONS system')
ps.add_argument("path", type=str, nargs="+", help='Path to csv or folder of csv\'s to be plotted')
ps.add_argument("-f", "--fix", action="store_true", help="Fix aspect ratio/scale of graph")
ps.add_argument("-s", "--speed", action="store_true", help="Graph speed with marker color")

# mirror x/y option
# date range / animate
# stats page thing
# titles?

cmin=0
cmax=0

args=ps.parse_args()
if args.fix:
	layout = go.Layout(scene=dict(aspectmode='data'))
else:
	layout=go.Layout()
fig=go.Figure(layout=layout)
cent={'X':0,'Y':0,'Z':0}
cent=pd.DataFrame(np.array([[0,0,0]]),columns=['X', 'Y', 'Z'])
fig.add_trace(go.Scatter3d(x=cent['X'], y=cent['Y'], z=cent['Z'], mode='markers', marker=dict(size=5, color='orange'), name="Center"))

ranges=[]

try:
	for csv in args.path:
		orbit=pd.read_csv(csv)
		orbit=orbit.loc[:, ~orbit.columns.str.contains('^Unnamed')]
		orbit.rename(columns=lambda i: i.strip(), inplace=True)
		orbit.dropna(inplace=True)
		if args.speed:
			orbit['TotalSpeed'] = (abs(orbit.VX)+abs(orbit.VY)+abs(orbit.VZ))
			il=[min(orbit['TotalSpeed']), max(orbit['TotalSpeed'])]
			if il[0]>cmin:
				cmin=il[0]
			if il[1]>cmax:
				cmax=il[1]

			fig.add_trace(go.Scatter3d(x=orbit['X'], y=orbit['Y'], z=orbit['Z'], mode='markers', marker=dict(size=1, color=orbit['TotalSpeed'], colorscale='bluered'), name=csv))
		else:

			fig.add_trace(go.Scatter3d(x=orbit['X'], y=orbit['Y'], z=orbit['Z'], mode='markers', marker=dict(size=1), name=csv))

except FileNotFoundError as error:
	print("Error: "+csv+" could not be read as a csv")
	exit()
if args.speed:
	fig.update_traces(marker=dict(cmin=cmin, cmax=cmax))
fig.update_traces(marker=dict(size=1))
fig.show()