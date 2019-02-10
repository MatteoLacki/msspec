import numpy as np
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None
try:
    import plotly
except ModuleNotFoundError:
    plotly = None

from msspec.misc import repr_long_list
    


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
        return sum(np.abs(self.i))

    def trim_below(self, min_intensity):
        """Trim intensities below the provided cut off.
        
        Args:
            min_intensity (float): The intensity below which all peaks are trimmed.
        """
        self.mz = self.mz[self.i >= min_intensity]
        self.i = self.i[self.i >= min_intensity]

    def __repr__(self):
        """Represent the spectrum."""
        return "Spectrum.mz\t\t{0}\nSpectrum.intensity\t{1}\n".format(
            repr_long_list(self.mz),
            repr_long_list(self.i))

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
        if plt:
            plt.style.use(plt_style)
            plt.vlines(x=self.mz,
                       ymin=[0],
                       ymax=self.i,
                       colors=peak_color)
            if show:
                plt.show()
        else:
            print("Install matplotlib to use this function.")

    def plotly(self, path='spectrum.html', webgl=True, show=True):
        """Make a plotly plot."""
        if plotly:
            color = 'black'
            mz = np.insert(self.mz, 0, 0)
            i = np.insert(self.i, 0, 0)
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

            plotly.offline.plot(fig, filename=path, auto_open=show)
        else:
            print('Install the plotly module.')



def test_spectrum():
    s = Spectrum([1,3,2], [10,20,30])
    s.plot()
    s.plotly()
    s.sort()
    assert all(s.mz == np.array([1,2,3]))
    assert all(s.i == np.array([10,30,20]))
    s.trim_below(15)
    assert all(s.mz == np.array([2,3]))
    assert all(s.i == np.array([30,20]))
