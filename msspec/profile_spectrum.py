import matplotlib.pyplot as plt
from itertools import cycle

from msspec.spectrum import Spectrum
from msspec.cluster.bitonic import bitonic
from msspec.cluster.zeros import zeros
from msspec.cluster.zeros_bitonic import zeros_bitonic

class ProfileSpectrum(Spectrum):
    """A profile (raw) spectrum."""

    def centroiding(self, clustering=zeros_bitonic):
        for M, I in clustering(self.mz, self.i):
            print(M,I)

    def plot(self,
             plt_style = 'dark_background',
             peak_color= 'greenyellow',
             clustering = zeros_bitonic,
             colors    = ('red', 'yellow','blue', 'white'),
             show      = True):
        super().plot(plt_style, peak_color, show=False)
        cols = []
        mz = []
        for (M, I), (i, c) in zip(clustering(self.mz, self.i),
                                  enumerate(cycle(colors))):
            cols.extend([c]*len(M))
            mz.extend(M)
        plt.scatter(x=mz, y=[0]*len(mz), c=cols)
        if show:
            plt.show()
