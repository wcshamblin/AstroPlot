#!/usr/bin/python3
import plotly.graph_objects as go
import pandas as pd
import argparse
import numpy as np
import warnings
ps = argparse.ArgumentParser(description='Parses and plots data from JPL\'s HORIZONS system')
ps.add_argument("path", type=str, nargs="+", help='Path to csv or folder of csv\'s to be plotted')
ps.add_argument("-f", "--fix", action="store_true", help="Fix aspect ratio/scale of graph")
ps.add_argument("-s", "--speed", action="store_true", help="Graph speed with marker color")
ps.add_argument("-b", "--black", action="store_true", help="Use a black background color")

# stats page thing
# titles?
# convert units

cmin=0
cmax=0
lcol="black"
startn=0

args=ps.parse_args()

fig=go.Figure()

fig.update_traces(marker=dict(size=1))

if args.fix:
	fig.update_layout(scene=dict(aspectmode='data'))

if args.black:
	lcol="white"
	fig.update_layout(scene = dict(
	                    xaxis = dict(
	                         backgroundcolor="black",
	                         gridcolor="gray",
	                         showbackground=True,
	                         zerolinecolor="gray",),
	                    yaxis = dict(
	                        backgroundcolor="black",
	                        gridcolor="gray",
	                        showbackground=True,
	                        zerolinecolor="gray"),
	                    zaxis = dict(
	                        backgroundcolor="black",
	                        gridcolor="gray",
	                        showbackground=True,
	                        zerolinecolor="gray",),),
	                    paper_bgcolor="black")
fig.update_layout(legend=dict(font=dict(color=lcol),x=0, y=1),margin=dict(r=0,l=0,b=0,t=0))

cent={'X':0,'Y':0,'Z':0}
cent=pd.DataFrame(np.array([[0,0,0]]),columns=['X', 'Y', 'Z'])
fig.add_trace(go.Scatter3d(x=cent['X'], y=cent['Y'], z=cent['Z'], mode='markers', marker=dict(size=5, color='orange')))

ranges=[]

for csv in args.path:
	inf=[]
	title=csv
	try:
		orbit=open(csv, "r")
	except IOError as error:
		print("Error: "+csv+" could not be read as a csv")
		exit()

	for i in range(0,22):
		line=orbit.readline()
		inf.append(line)
		if "$$SOE" in line:
			orbit.seek(i-2)
			startn=i-2
			break
	
	orbit=pd.read_csv(orbit,skiprows=startn)
	orbit=orbit.loc[:, ~orbit.columns.str.contains('^Unnamed')]
	orbit.rename(columns=lambda i: i.strip(), inplace=True)
	orbit.dropna(inplace=True)

	for line in inf:
		if "Target body name:" in line:
			title=line.split("Target body name:")[1].split("{source:")[0]

	# orbit['Calendar Date (TDB)']=orbit['Calendar Date (TDB)'].str.replace('A.D. ', '')
	# orbit['Calendar Date (TDB)']=pd.to_datetime(orbit['Calendar Date (TDB)'])
	# print(orbit['Calendar Date (TDB)'])
	# test=orbit['Calendar Date (TDB)']

	if args.speed:
		try:
			orbit['TotalSpeed'] = (abs(orbit['VX'])+abs(orbit['VY'])+abs(orbit['VZ']))
		except KeyError as error:
			warnings.warn("Velocity components not available for "+csv+", unable to display speed.")
			fig.add_trace(go.Scatter3d(x=orbit['X'], y=orbit['Y'], z=orbit['Z'], mode='markers', marker=dict(size=1), name=title))
		else:
			il=[min(orbit['TotalSpeed']), max(orbit['TotalSpeed'])]
			if il[0]>cmin:
				cmin=il[0]
			if il[1]>cmax:
				cmax=il[1]
			fig.add_trace(go.Scatter3d(x=orbit['X'], y=orbit['Y'], z=orbit['Z'], mode='markers', marker=dict(size=1, color=orbit['TotalSpeed'], colorscale='bluered'), name=title))
		
	else:
		fig.add_trace(go.Scatter3d(x=orbit['X'], y=orbit['Y'], z=orbit['Z'], mode='markers', marker=dict(size=1), name=csv))
if args.speed:
	fig.update_traces(marker=dict(cmin=cmin, cmax=cmax))
fig.show()