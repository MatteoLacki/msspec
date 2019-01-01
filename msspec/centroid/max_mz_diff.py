def max_mz_diff(spectrum, min_mz_diff=1.5):
    """Cluster points based on the distance between them.

    Args:
        spectrum (msspec.Spectrum): An instance of the mass spectrum.
        min_mz_diff (float): The minimal m/z difference that separates clusters.
    Yields:
        Tuples of masses and intensities.
    """
    m_ = spectrum.mz[0]
    M = []
    I = []
    for _m,_i in spectrum:
        if _m - m_ >= min_mz_diff:
            yield M, I
            M = []
            I = []
        else:
            M.append(_m)
            I.append(_i)
        m_ = _m
