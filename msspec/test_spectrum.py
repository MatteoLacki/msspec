from msspec.read.txt import read_txt
from msspec.spectrum import Spectrum

from masstodon.data.substance_p_wv_1_5_wh_4500 import mz, i

s = Spectrum(mz, i)
# s.plot() # OK
# s.plotly()


import plotly
import numpy as np

color = 'black'

# adding zero for clarity.
mz = np.insert(s.mz, 0, 0)
i = np.insert(s.i, 0, 0)
t = ["{}  {}".format(round(MZ,4),int(I)) for MZ,I in zip(mz,i)]

go = plotly.graph_objs
bars = go.Bar(x=mz, y=i, 
              marker={'color':color},
              text=t,
              hoverinfo='text')
points = go.Scatter(x=mz,y=i,
                    mode='markers',
                    marker={'color':color, 'size':1},
                    text=t,
                    hoverinfo='text')
layout = go.Layout(showlegend=False,
                   hovermode='closest',
                   autosize=True)
fig = go.Figure(data=[bars, points], layout=layout)
plotly.offline.plot(fig, auto_open=True)

p='/Users/matteo/Projects/masstodon/data/Belgian/2013_05_01/SUBP/SubP_ETD_010513_206_WH35_WV300_cal_cent.txt'

from msspec.read.txt import read_txt

mz, i = read_txt(p)