%load_ext autoreload
%autoreload 2

from msspec.read.txt import read_txt
from msspec.spectrum import Spectrum

from masstodon.data.substance_p_wv_1_5_wh_4500 import mz, i

s = Spectrum(zip(mz, i))

n = Spectrum([(10,10), (200,300), (40, 100)])
m = Spectrum([( 1,10), (200,300), (40, 100), (204, 3)])

# add centroiding!
## test on an orbitrap spectrum
## test on an synapt raw spectrum
## investigate the code from Joshua.