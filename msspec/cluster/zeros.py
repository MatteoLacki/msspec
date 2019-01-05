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
