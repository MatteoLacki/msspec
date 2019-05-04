"""All these methods assume the peaks to be sorted by m/z ratios."""
from math import inf


def pure_mz_sep(peaks, mz_sep=1.5):
    """Cluster points based on the distance between them.

    Args:
        peaks (iterable): tuples of m/z ratios and intensities.
        mz_sep (float): Seperating distance between consecutive peaks.
    Yields:
        Lists of peaks.
    """
    m_ = inf
    P = []
    for _m, i in peaks:
        if _m - m_ >= mz_sep:
            yield P
            P = []
        P.append((_m, i))
        m_ = _m
    yield P


def pure_bitonic(peaks):
    """Cluster by intensity going up and down.

    Args:
        peaks (iterable): tuples of m/z ratios and intensities.
        mz_sep (float): Seperating distance between consecutive peaks.
    Yields:
        Lists of peaks.
    """
    P = []
    i__ = -2
    _i_ = -1
    for __m, __i in peaks:
        if i__ > _i_ < __i:
            yield P
            P = []
        P.append((__m, __i))
        i__, _i_ = _i_, __i
    yield P


def intensity_watershed(peaks, minimal_intensity=0):
    """Cluster consecutive peaks surrounded by smaller ones.

    Args:
        peaks (iterable): tuples of m/z ratios and intensities.
        minimal_intensity (float): the minimal intensity above which a cluster can appear.
    Yields:
        Lists of peaks.
    """
    P = []
    for m, i in peaks:
        if i <= minimal_intensity:
            if P:
                yield P
                P = []
        else:
            P.append((m,i))
    if P:
        yield P
