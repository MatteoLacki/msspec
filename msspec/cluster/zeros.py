def zeros(mz, i):
    """Cluster based on regions between zero intensities.
    
    Args:
        mz (iterable): m/z ratios.
        i (iterable): Intensities.
    """
    M = []
    I = []
    for _m, _i in zip(mz, i):
        if _i == 0:
            if len(M) > 0:
                yield M, I
                M = []
                I = []
        else:
            M.append(_m)
            I.append(_i)
    if len(M) > 0:
        yield M, I

def test_zeros():
    mz = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    i =  [0 ,0, 1, 2, 0, 0, 2, 3, 0]
    o = list(zeros(mz, i))
    r = [([2, 3],
          [1, 2]),
         ([6, 7],
          [2, 3])]
    assert o == r
