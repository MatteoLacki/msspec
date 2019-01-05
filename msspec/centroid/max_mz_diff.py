def max_mz_diff(mz, i, min_mz_diff=1.5):
    """Cluster points based on the distance between them.

    Args:
        mz (iterable): m/z ratios.
        i (iterable): Intensities.
        min_mz_diff (float): The minimal m/z difference that separates clusters.
    Yields:
        Tuples of m/z ratios and intensities.
    """
    M = []
    I = []
    m_ = next(mz.__iter__i()) - min_mz_diff/2.0
    for _m, _i in zip(mz, i):
        if _m - m_ >= min_mz_diff:
            yield M, I
            M = []
            I = []
        M.append(_m)
        I.append(_i)
        m_ = _m
    yield M, I
