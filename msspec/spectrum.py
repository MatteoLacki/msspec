"""Spectrum: a collection of peaks and some actions on them."""
from . import plotly, plt
from .misc import mix


class Spectrum(object):
    """A mass spectrum."""

    def __init__(self, peaks):
        """Initialize the spectrum.
        Args:
            peaks (iterable): A series of pairs (m/z, intensity).
        """
        self.peaks = list(peaks)
        self.peaks.sort()

    def copy(self):
        """Copy the class."""
        return self.__class__(self.peaks.copy())

    def __add__(self, other):
        """Add two spectra."""
        return self.__class__(mix(self.peaks, other.peaks))

    def __iadd__(self, other):
        """Add the other spectrum to this one."""
        self.peaks = list(mix(self.peaks, other.peaks))
        return self

    def drop_zero_peaks(self):
        """Drop the entries with zero intensities."""
        self.peaks = [(m,i) for m,i in self if i != 0]

    def __iter__(self):
        """Iterate over peaks in the spectrum."""
        return self.peaks.__iter__()

    def __len__(self):
        """Get the number of peaks."""
        return len(self.peaks)

    def total_ion_current(self):
        """Count the total intensity in the spectrum."""
        return sum(abs(i) for m,i in self.peaks)

    def trim_below(self, min_intensity):
        """Trim intensities below the provided cut off.
        
        Args:
            min_intensity (float): The intensity below which all peaks are trimmed.
        """
        self.peaks = [(m,i) for m,i in self.peaks if i>= min_intensity]

    def replace_below_with_zeros(self, min_intensity):
        """Replace intensities below min_intensity with 0."""
        self.peaks = [(m,i if i>=min_intensity else 0.0) for m,i in self.peaks]

    def __repr__(self):
        """Represent the spectrum."""
        m0,i0 = self.peaks[0]
        mN,iN = self.peaks[-1]
        return "Spectrum({}|{} {}|{})".format(m0,i0,mN,iN)

    def centroid(self, resolution):
        raise NotImplementedError

    def plot(self, col_peak='lightgreen',show=True):
        """Make a simple visualization of a mass spectrum.
        Args:
            col_peak (str): A color to visualize the peaks.
            show (bool): Show the figure, or just add it to the canvas.
        """
        if plt:
            mz, i = tuple(zip(*self.peaks))
            plt.vlines(x=mz, ymin=[0], ymax=i, colors=col_peak)
            # plt.vlines(x=mz, ymin=[0], ymax=i)
            if show:
                plt.show()
        else:
            print("Install matplotlib to use this function.")

    def plotly(self, path='spectrum.html', show=True, digits=4):
        """Make a plotly plot."""
        if plotly:
            color = 'black'
            mz = [0]
            i = [0]
            t = [""]
            for M,I in self.peaks:
                mz.append(M)
                i.append(I)
                t.append("{}  {}".format(round(M, digits), int(I)))
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
            plotly.offline.plot(fig, filename=path, auto_open=show)
        else:
            print('Install the plotly module.')


