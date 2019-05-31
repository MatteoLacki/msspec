from pathlib import Path

from msspec.read.txt import read_txt
from msspec.read.txt import read_txt
it = mzxml.read("/Users/matteo/Projects/masstodon/data/FRL_220715_ubi_714_ETD_20.mzXML")

datapath = Path("/Users/matteo/Projects/masstodon/data/Belgian/2015_07/UBI_ORBI/UBI_9plus_ETD_100715")
MZ, I = read_txt(datapath/"FRL_100715_UBI_952_01.txt")