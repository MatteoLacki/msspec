%load_ext autoreload
%autoreload 2

import numpy as np

from msspec import plotly, plt
from msspec.read.txt import read_txt
from msspec.spectrum import Spectrum
from msspec.centroided import CentroidedSpectrum

from masstodon.data.substance_p_wv_1_5_wh_4500 import mz, i 

synapt = mz, i
mz = np.array(mz)
I = np.array(i)
s = Spectrum(zip(*synapt))
s.plot()

cs = CentroidedSpectrum(mz-.01, mz+.01, I)
# the point is now to make classes, that differ in the way they 
# make the centroided spectra.


from msspec.read.resolution import parse as parse_resolution


class CountSpectrum(Spectrum):
    """A spectrum with intensities being counts.

    These sort of spectra correspond to Waters mass spectra.
    """
    def centroid(self, resolution='10ppm'):
        pass

class FourierSpectrum(Spectrum):
    """A spectrum with intensities proportional to corellations with the Fourier base."""
    pass




