from msspec.read.txt import read_txt

def write_txt(mz, i, path):
    """Write a spectrum to file.

    Args:
        mz (iterable): m/z ratios,
        i (iterable): Intensities.
        path (str): Target path.
    """
    with open(path, w) as f:
        for _m, _i in zip(mz, i):
            f.write("{}\t{}".format(_m, _i))

def test_write_txt():
    mz = [1,2,3]
    i = [4,5,4]
    write("spec.txt")
    mz2, i2 = read_txt("spectrum.txt")
    assert mz == mz2
    assert i == i2

