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
        for (M, I), col in zip(clustering(self.mz, self.i),
                               cycle(colors)):
            plt.scatter(x=M, y=[0]*len(M), c=col)
        if show:
            plt.show()
