%load_ext autoreload
%autoreload 2

from msspec.read.txt import read_txt
from msspec.spectrum import Spectrum

from masstodon.data.substance_p_wv_1_5_wh_4500 import mz, i

s = Spectrum(zip(mz, i))
w = s.copy()
w.trim_below(100)

len(w)
len(s)
s.plot()
# finally, the pairs instead of some np.arrays.