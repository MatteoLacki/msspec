def zeros(peaks):
    """Cluster based on regions between zero intensities.
    
    Args:
        mz (iterable): m/z ratios.
        i (iterable): Intensities.
    """
    M = []
    I = []
    for _m, _i in peaks:
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
    o = list(zeros(zip(mz, i)))
    r = [([2, 3],
          [1, 2]),
         ([6, 7],
          [2, 3])]
    assert o == r


#TODO: rewrite as a ufunc.
def zero_cluster_orbi(peaks, agg='max'):
    """Return aggregated values for orbitrap data."""
    m_agg = 0.0
    i_sum = 0.0
    prev_i = 0.0
    i_max = 0.0
    for mz, i in peaks:
        if i > 0:
            m_agg += mz*i
            i_sum += i
            i_max = max(i_max, i)
        else:
            if prev_i > 0.0:
                yield (m_agg/i_sum, i_max)
                m_agg = 0.0
                i_sum = 0.0
                i_max = 0.0
        prev_i = i
    if i_sum > 0:
        yield (m_agg/i_sum, i_max)