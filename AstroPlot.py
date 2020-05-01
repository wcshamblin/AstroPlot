#!/usr/bin/python3
import plotly.graph_objects as go
import pandas as pd
import argparse
import numpy as np
import warnings
ps = argparse.ArgumentParser(description='Parses and plots data from JPL\'s HORIZONS system')
ps.add_argument("path", type=str, nargs="+", help='Path to csv or folder of csv\'s to be plotted')
ps.add_argument("-r", "--relative", action="store_true", help="Use non-symmetrical graph axis, scaled to data")
ps.add_argument("-s", "--speed", action="store_true", help="Graph speed with marker color")
ps.add_argument("-w", "--white", action="store_true", help="Use a white background color")
ps.add_argument("-c", "--convert", type=str, help="Convert CSV position/speed units into this unit (KM-S, KM-D, AU-D)")


cmin=0
cmax=0
lcol="black"
startn=0

args=ps.parse_args()

fig=go.Figure()

fig.update_traces(marker=dict(size=1))
if args.convert is not None:
	args.convert=args.convert.lower()
	if args.convert not in ["km-s", "au-d", "km-d"]:
		warnings.warn("Unit not recognized. Use one of the following: KM-S, AU-D, KM-D. Not attempting to convert.")
		args.convert=None

if not args.relative:
	fig.update_layout(scene=dict(aspectmode='data'))

if not args.white:
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
else:
	fig.update_layout(scene = dict(
	                    xaxis = dict(
	                         backgroundcolor="white",
	                         gridcolor="gray",
	                         showbackground=True,
	                         zerolinecolor="gray",),
	                    yaxis = dict(
	                        backgroundcolor="white",
	                        gridcolor="gray",
	                        showbackground=True,
	                        zerolinecolor="gray"),
	                    zaxis = dict(
	                        backgroundcolor="white",
	                        gridcolor="gray",
	                        showbackground=True,
	                        zerolinecolor="gray",),),
	                    paper_bgcolor="white")
fig.update_layout(legend=dict(font=dict(color=lcol),x=0, y=1),margin=dict(r=0,l=0,b=0,t=0))

cent={'X':0,'Y':0,'Z':0}
cent=pd.DataFrame(np.array([[0,0,0]]),columns=['X', 'Y', 'Z'])
fig.add_trace(go.Scatter3d(x=cent['X'], y=cent['Y'], z=cent['Z'], mode='markers', marker=dict(size=5, color='orange')))

ranges=[]

for csv in args.path:
	inf=[]
	title=csv
	center=[0,0,0]
	units=""
	try:
		orbit=open(csv, "r")
	except IOError as error:
		print("Error: "+csv+" could not be read as a csv")
		exit()

	for i in range(0,40):
		line=orbit.readline()
		inf.append(line)
		if "$$SOE" in line:
			startn=i-2
			break
	orbit.seek(0)
	orbit=pd.read_csv(orbit,skiprows=startn)
	orbit=orbit.loc[:, ~orbit.columns.str.contains('^Unnamed')]
	orbit.rename(columns=lambda i: i.strip(), inplace=True)
	orbit.dropna(inplace=True)

	for line in inf:
		if "Target body name:" in line:
			title=(line.split("Target body name:")[1].split("{")[0]).strip()
		if "Center geodetic :" in line:
			center=[float(i) for i in ((line.split("Center geodetic :")[1].split("{")[0]).strip()).split(",")]
		if "Output units    :" in line:
			units=(line.split("Output units    :")[1].split("{")[0]).strip().lower()

	if args.convert is not None and units == "":
		warnings.warn("No units declaration in "+csv+", not attempting to convert")

	else:
		if args.convert is not None:
			if args.convert!=units:
				print(csv+" has "+units.upper()+", converting to "+args.convert.upper())
				if args.convert[:2]!=units[:2]:
					if args.convert[:2]=="km":
						orbit['X']=orbit['X']*149597870.7
						orbit['Y']=orbit['Y']*149597870.7
						orbit['Z']=orbit['Z']*149597870.7
					else:
						orbit['X']=orbit['X']/149597870.7
						orbit['Y']=orbit['Y']/149597870.7
						orbit['Z']=orbit['Z']/149597870.7
				if args.speed:
					if set(['VX', 'VY', 'VZ']).issubset(orbit.columns):
						if args.convert[:2]=="km": # au -> km
							orbit['VX']=orbit['VX']*149597870.7
							orbit['VY']=orbit['VY']*149597870.7
							orbit['VZ']=orbit['VZ']*149597870.7
						else:                      # km -> au
							orbit['VX']=orbit['VX']/149597870.7
							orbit['VY']=orbit['VY']/149597870.7
							orbit['VZ']=orbit['VZ']/149597870.7
						if args.convert[3]=="s":
							orbit['VX']=orbit['VX']/86400
							orbit['VY']=orbit['VY']/86400
							orbit['VZ']=orbit['VZ']/86400
						else:
							orbit['VX']=orbit['VX']*86400
							orbit['VY']=orbit['VY']*86400
							orbit['VZ']=orbit['VZ']*86400
					else:
						warnings.warn("Velocity component not present in "+csv+", not able to convert")

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
		fig.add_trace(go.Scatter3d(x=orbit['X'], y=orbit['Y'], z=orbit['Z'], mode='markers', marker=dict(size=1), name=title))
if args.speed:
	fig.update_traces(marker=dict(cmin=cmin, cmax=cmax))
fig.show()