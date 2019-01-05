from itertools import islice, chain
from math import inf
import numpy as np


def bitonic(mz, i, tol=0, multiplier=1.1, 
            buffer_len=40, verbose=False):
    """Cluster based on bitonicity of the intensity.

    Args:
        mz (iterable): m/z ratios (assumed positive).
        i (iterable): Intensities (assumed positive).
        tol (float): The minimal m/z difference that separates clusters.
        multiplier (float): How much more tolerance is acceptible to tell peaks apart?
        buffer_len (int): The number of m/z in the buffer.
        verbose (bool): Verbose mode?
    Yields:
        Tuples of m/z ratios and intensities.
    """
    mz_buffer = list(islice(mz, buffer_len))
    if not tol: # predicting initial tol:
        tol = np.median(np.diff(mz_buffer)) * multiplier
        if verbose:
            print("Tolerance set to {}.".format(tol))
    mz = chain(mz_buffer, mz) 
    # setting up guardians
    m__ = -inf
    _m_ = mz_buffer[0] - tol/2.0
    i__ = -2
    _i_ = -1
    M = []
    I = []
    for __m,__i in zip(mz, i):
        if (__m - _m_ > tol) or (i__ > _i_ < __i and _m_ - __m <= tol):
        # if i__ > _i_ < __i and 
            yield M, I
            if len(M)>2:
                tol = np.median(np.diff(M))*multiplier
                if verbose:
                    print(tol)
            M = []
            I = []
        M.append(__m)
        I.append(__i)
        m__, _m_ = _m_, __m
    yield M, I


def test_bitonic():
    mz = [0.00,0.01,0.02,0.03,1.00,1.01,1.02,1.03,1.04,3.00]
    i  = [1000,1200,1300,1100, 500,1000,2000,1000, 300, 100]

    o = list(bitonic(mz, i, .02))
    r = [([0.00,0.01,0.02,0.03],[1000,1200,1300,1100]),
         ([1.00,1.01,1.02,1.03,1.04],[500,1000,2000,1000, 300]),
             ([3.00],[100])]
    assert o == r

    o = list(bitonic(mz, i))
    o = list(bitonic((m for m in mz), i))
