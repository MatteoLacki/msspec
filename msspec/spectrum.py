"""Spectrum: a collection of peaks and some actions on them."""

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None
try:
    import plotly
except ModuleNotFoundError:
    plotly = None


class Spectrum(object):
    """A mass spectrum."""

    def __init__(self, mz_i):
        """Initialize the spectrum.
        Args:
            mz_i (iterable): A series of pairs (m/z, intensity).
        """
        self.peaks = list(mz_i)

    def copy(self):
        """Copy the class."""
        return self.__class__(self.peaks.copy())

    def __add__(self, other):
        """Add two spectra."""
        pass

    def sort(self, reverse=False):
        """Sort the spectrum by increasing m/z values."""
        self.peaks.sort(reverse=reverse)

    def drop_zero_peaks(self):
        """Drop the entries with zero intensities."""
        self.peaks = [(m,i) for m,i in self if i != 0]

    def __iter__(self):
        """Iterate over peaks in the spectrum."""
        yield self.peaks

    def __len__(self):
        """Get the number of peaks."""
        return len(self.peaks)

    def l1(self):
        """Count l1 norm of intensities."""
        return sum(abs(i) for m,i in self.peaks)

    def trim_below(self, min_intensity):
        """Trim intensities below the provided cut off.
        
        Args:
            min_intensity (float): The intensity below which all peaks are trimmed.
        """
        self.peaks = [(m,i) for m,i in self.peaks if i>= min_intensity]

    def __repr__(self):
        """Represent the spectrum."""
        m0,i0 = self.peaks[0]
        mN,iN = self.peaks[-1]
        return "Spectrum[({}, {})..({}, {})]".format(m0,i0,mN,iN)

    def plot(self,
             plt_style='dark_background',
             col_peak='greenyellow',
             show=True):
        """Make a simple visualization of a mass spectrum.
        
        Args:
            plt_style (str): The style of the matplotlib visualization. Check https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
            col_peak (str): A color to visualize the peaks.
            show (bool): Show the figure, or just add it to the canvas.
        """
        if plt:
            mz, i = tuple(zip(*self.peaks))
            plt.style.use(plt_style)
            plt.vlines(x=mz, ymin=[0], ymax=i,colors=col_peak)
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
