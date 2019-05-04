%load_ext autoreload
%autoreload 2
import matplotlib.pyplot as plt
from itertools import cycle

from msspec.read.txt import read_txt
from msspec.spectrum import Spectrum
from masstodon.data.substance_p_wv_1_5_wh_4500 import mz, i
from msspec.cluster.pure_mz_sep import pure_mz_sep


path = "/Users/matteo/Projects/masstodon/data/FRL_220715_ubi_714_ETD_20.mzXML"
spectrum = next(read_mzml(path, scan=1))


s = Spectrum(zip(spectrum['m/z array'],
                 spectrum['intensity array']))
# s.plot() # OK
# s.plotly() # orbitrap data too complicated for this html plotting
len(list(pure_mz_sep(s.peaks, 1.5)))

clustering = pure_mz_sep
clustering = pure_bitonic
clustering = intensity_watershed

colors = ('red', 'green','orange', 'blue', 'yellow')
for peaks, col in zip(clustering(s.peaks), cycle(colors)):
    Spectrum(peaks).plot(show=False, col_peak=col)
plt.show()
s.plot(col_peak='red')
%%timeit
x = intensity_watershed(s.peaks)

# should we continue with this?
mz, intensity = spectrum['m/z array'], spectrum['intensity array']
mz = mz[intensity > 0]
intensity = intensity[intensity > 0]
x = list(pure_bitonic(zip(mz, intensity)))


# Good, so now we can have the first sensible go at a centroiding procedure.
import numpy as np

# get a weighted median
np.median(list(m for m,i in x[0]))







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