#!/usr/bin/python3
import plotly.graph_objects as go
import pandas as pd
import argparse
import numpy as np
ps = argparse.ArgumentParser(description='Parses and plots data from JPL\'s HORIZONS system')
ps.add_argument("path", type=str, nargs="+", help='Path to csv or folder of csv\'s to be plotted')
ps.add_argument("-f", "--fix", action="store_true", help="Fix aspect ratio/scale of graph")
ps.add_argument("-s", "--speed", action="store_true", help="Graph speed with marker color")
ps.add_argument("-b", "--black", action="store_true", help="Use a black background color")
ps.add_argument("-a", "--animate", type=str, help="Trace to animate, same format as <path>")
# date range / animate
# stats page thing
# titles?
# convert units

cmin=0
cmax=0

args=ps.parse_args()


animtarget="./orbits/starman.txt"
anim=pd.read_csv(animtarget)
anim=anim.loc[:, ~anim.columns.str.contains('^Unnamed')]
anim.rename(columns=lambda i: i.strip(), inplace=True)
anim.dropna(inplace=True)

# frames=[dict(data=[dict(x=anim['X'], 
#                         y=anim['Y'],
#                         z=anim['Z'], 
#                         mode='markers', 
#                         type='scatter3d',
#                         marker=dict(color='white', size=10),
#                         name=str(k)
#                         )
#                   ]) for k in range(0, len(anim.index), 20)]
frames=[
    go.Frame(data=go.Scatter3d(
    x=[row['X']],
    y=[row['Y']],
    z=[row['Z']]),
    name=str(index))
    for index, row in anim.iterrows()]
    #for k in range(len(anim.index))]

def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

fig=go.Figure(frames=frames)

sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]


fig.update_traces(marker=dict(size=1))

if args.black:
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
	                    paper_bgcolor="black", legend=dict(font=dict(color="white"))
	                  )

fig.update_layout(margin=dict(r=0,l=0,b=0,t=0),legend=dict(x=0,y=1),updatemenus=[{'type': 'buttons',
                           'buttons': [{'label': '&#9654;',
                                        'method': 'animate',
                                        'args': [None, frame_args(500)]},
                                       {'label': '&#9724;',
                                        'method': 'animate',
                                        'args': [None, frame_args(0)]}
                                        ]}], sliders=sliders)
cent={'X':0,'Y':0,'Z':0}
cent=pd.DataFrame(np.array([[0,0,0]]),columns=['X', 'Y', 'Z'])
fig.add_trace(go.Scatter3d(x=cent['X'], y=cent['Y'], z=cent['Z'], mode='markers', marker=dict(size=5, color='orange')))

ranges=[]

try:
	for csv in args.path:
		orbit=pd.read_csv(csv)
		orbit=orbit.loc[:, ~orbit.columns.str.contains('^Unnamed')]
		orbit.rename(columns=lambda i: i.strip(), inplace=True)
		orbit.dropna(inplace=True)

		# orbit['Calendar Date (TDB)']=orbit['Calendar Date (TDB)'].str.replace('A.D. ', '')
		# orbit['Calendar Date (TDB)']=pd.to_datetime(orbit['Calendar Date (TDB)'])
		# print(orbit['Calendar Date (TDB)'])
		# test=orbit['Calendar Date (TDB)']

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
if args.fix:
	fig.update_layout(scene=dict(aspectmode='data'))

fig.show()