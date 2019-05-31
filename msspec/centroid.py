import numpy as np

from . import plotly, plt
from .non_overlapping_intervals import OpenClosed
from .read.resolution import parse as parse_resolution


class CentroidedSpectrum(object):
    """A class storing centroided spectrum.

    It supports quick, vectorized lookups."""
    def __init__(self, mzL, mzR, I, intervals=OpenClosed):
        """
        Args:
            mzL (iterable): left ends of intervals.
            mzR (iterable): right ends of intervals.
            I (iterable): intensities.
            intervals (NonOverlappingIntervals): choice of intervals.
        """
        self.I = np.array(I)
        self.mz = intervals(mzL, mzR)

    def __getitem__(self, mz):
        i = self.mz[mz]
        return np.where(i > 0, self.I[i], 0)

    def __repr__(self):
        return "CentroidedSpectrum({:.2f}^{:.0f}^{:.2f}__{:.2f}^{:.0f}^{:.2f})".format(
            self.mz.L[0],
            self.I[0],
            self.mz.R[0],
            self.mz.L[-1],
            self.I[-1],
            self.mz.R[-1])

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



def centroid(peaks, resolution='10ppm'):
    """Run a simple centroiding with a given resolution.
    Args:
        peaks (iterable): tuples of m/z and intensity.
        resolution (str or float): the resolution of resulting peaks.
    """ 
    thr, thr_type = parse_resolution(resolution)
    peaks = filter(lambda x: x[1]>0, peaks)
    mz_, i_ = next(peaks)
    thr2 = thr if thr_type == "abs" else thr*mz_
    L = [mz_ - thr2]
    R = []
    I = []
    # we work on the current peak peak_, not on _peak
    for _mz, _i in peaks:
        if _mz - mz_ <= 2.0*thr2:
            # Overlaying peaks? Big one scoops proportionally more m/z.
            mid_mz = mz_ + (_mz - mz_)*i_/(i_+_i)
            R.append(mid_mz)
            L.append(mid_mz)
        else:
            R.append(mz_ + thr2)
            L.append(_mz - thr2)
        mz_ = _mz
        thr2 = thr if thr_type == "abs" else thr*mz_
        I.append(i_)
        i_ = _i
    R.append(mz_ + thr2)
    I.append(i_)
    return CentroidedSpectrum(L, R, I)


def test_centroid():
    """Test the simple centroiding."""
    # testing absolute spectrum
    peaks = [(10, 0), (11,1), (12,2),(13,1),(20,3),(21,1)]
    cs = centroid(peaks, '2da')
    assert cs.mz.L[0] == 9
    assert cs.mz.R[0] == 11+1/3
    assert cs.mz.L[1] == 11+1/3
    assert cs.mz.R[1] == 12+2/3
    assert cs.mz.L[2] == 12+2/3
    assert cs.mz.R[2] == 15
    assert cs.mz.L[3] == 18
    assert cs.mz.R[3] == 20+3/4
    assert cs.mz.L[4] == 20+3/4
    assert cs.mz.R[4] == 23
    # testing relative spectrum
    peaks = [(10, 0), (11,1), (12,2)]
    cs = centroid(peaks, '100000ppm')
    assert cs.mz.L[0] == 11-11/10
    assert cs.mz.R[0] == 11+1/3
    assert cs.mz.L[1] == 11+1/3
    assert cs.mz.R[1] == 12+12/10