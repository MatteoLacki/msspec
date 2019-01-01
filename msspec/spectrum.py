import numpy as np
try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except RuntimeError:
    matplotlib_available = False

from .misc import repr_long_list

class Spectrum(object):
    """A mass spectrum."""

    def __init__(self, mz=[], i=[]):
        """Initialize the spectrum.
        
        Args:
            mz (iterable): Recorded mass over charge ratios.
            i (iterable): Recorded intensities.
        """
        self.mz = np.array(mz)
        self.i = np.array(i)

    def sort(self):
        """Sort the spectrum by increasing m/z values."""
        I = np.argsort(self.mz)
        self.mz = self.mz[I]
        self.i = self.i[I]

    def drop_zero_peaks(self):
        """Drop the entries with zero intensities."""
        self.mz = self.mz[self.i != 0]
        self.i = self.i[self.i != 0]

    def __iter__(self):
        """Iterate over peaks in the spectrum."""
        yield from zip(self.mz, self.i)

    def l1(self):
        """Count l1 norm of intensities."""
        return sum(self.i)

    def trim(self, min_intensity):
        """Trim intensities below the provided cut off.
        
        Args:
            min_intensity (float): The intensity below which all peaks are trimmed.
        """
        self.mz = self.mz[self.i >= min_intensity]
        self.i = self.i[self.i >= min_intensity]

    def __repr__(self):
        """Represent the spectrum."""
        o = "Spectrum.mz\t\t{0}\nSpectrum.intensity\t{1}\n".format(
                repr_long_list(self.mz),
                repr_long_list(self.i))
        return o

    def plot(self,
             plt_style='dark_background',
             peak_color='greenyellow',
             show=True):
        """Make a simple visualization of a mass spectrum.
        
        Args:
            plt_style (str): The style of the matplotlib visualization. Check https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
            peak_color (str): A color to visualize the peaks.
            show (bool): Show the figure, or just add it to the canvas.
        """
        if matplotlib_available:
            plt.style.use(plt_style)
            plt.vlines(x=self.mz,
                       ymin=[0],
                       ymax=self.i,
                       colors=peak_color)
            if show:
                plt.show()
        else:
            print("Install matplotlib to use this function.")


def test_spectrum():
    s = Spectrum([1,3,2], [10,20,30])
    s.sort()
    assert all(s.mz == np.array([1,2,3]))
    assert all(s.i == np.array([10,30,20]))
    s.trim(15)
    assert all(s.mz == np.array([2,3]))
    assert all(s.i == np.array([30,20]))
