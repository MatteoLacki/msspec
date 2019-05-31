def zeros_bitonic(mz, i):
    """Cluster based on zeros and bitonic intensities.
    
    Args:
        mz (iterable): m/z ratios.
        i (iterable): Intensiities (contains the zero intensities),
    Yields:
        Tuples of m/z ratios and intensities within clusters.
    """
    M = []
    I = []
    i__ = -2
    _i_ = -1
    for __m, __i in peaks:
        if __i == 0 or i__ > _i_ < __i:
            if len(M) > 0:
                yield M, I
                M = []
                I = []
        if __i != 0:
            M.append(__m)
            I.append(__i)
        i__, _i_ = _i_, __i
    if len(M)>0:
        yield M, I

def test_zeros_bitonic():
    mz = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    i =  [0, 0, 1, 2, 3, 2, 0, 1, 4, 5, 3,  7,  3,  0 ]
    o = list(zeros_bitonic(zip(mz, i)))
    r = [([2, 3, 4, 5],
          [1, 2, 3, 2]),
         ([7, 8, 9, 10],
          [1, 4, 5, 3]),
         ([11, 12],
          [ 7,  3])]
    assert o == r
