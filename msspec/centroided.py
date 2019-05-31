import numpy as np

from . import plotly, plt
from .non_overlapping_intervals import OpenClosed


class CentroidedSpectrum(object):
    """A class storing centroided spectrum.

    It supports quick, vectorized lookups."""
    def __init__(self, mzL, mzR, I, intervals=OpenClosed):
        self.I = np.array(I)
        self.mz = intervals(mzL, mzR)

    def __getitem__(self, mz):
        i = self.mz[mz]
        return np.where(i > 0, self.I[i], 0)

    def plot(self, scatter=True, show=True, **kwds):
        """Plot the centroided spectrum."""
        if plt:
            if scatter:
                plt.scatter((self.mz.R+self.mz.L)/2, self.I)
            plt.bar(x=self.mz.L,
                    height=self.I,
                    width=self.mz.R-self.mz.L,
                    bottom=0,
                    align='edge',
                    **kwds)
            if show:
                plt.show()
        else:
            print("Install matplotlib to use this function.")