import numpy as np

"""
Here we solve the subproblem:

given nonoverlapping intervals (l1, r1) < .. < (lM, rM)
and a collection of points on the line X = (x0, x1, x2, .., xN) that
does not have to be sorted,
find for each xI the index I s.t. x in (lI, rI), or report -1.
"""

class Interval(object):
    """This class implements a collection of non-overlapping intervals."""
    def __init__(self, L, R, sorted=False):
        """Initialize the class.

        Arguments:
            L (iterable): the left ends of the intervals.
            R (iterable): the right end of the intervals.
            sorted (boolean): Are both L and R sorted?
        """
        L = np.array(L)
        R = np.array(R)
        if not sorted:
            L.sort()
            R.sort()
        assert (L < R).all()
        total_len = L.shape[0] + R.shape[0]
        self.LR = np.zeros(dtype=float, shape=(total_len,))
        self.LR[0::2] = L
        self.LR[1::2] = R

    @property
    def L(self):
        return self.LR[0::2]

    @property
    def R(self):
        return self.LR[1::2]

    def __getitem__(self, x):
        """Querry for x belonging to any of the intervals.

        Args:
            x (iterable): Point on the line that need to be classified.
        Results:
            np.array of ints: indices of intervals that the points belong to (intervals are now sorted). -1 corresponds to points outside any of the interval.
        """
        raise NotImplementedError


class OpenClosed(Interval):
    def __getitem__(self, x):
        """Querry for x belonging to any of the intervals.

        All intervals exclude the left end and include the right.
        """
        i = np.searchsorted(self.LR, x, side='left')
        cluster_no, in_clust = np.divmod(i, 2)
        cluster_no = np.where(in_clust, cluster_no, -1)
        return cluster_no


class ClosedOpen(Interval):
    def __getitem__(self, x):
        """Querry for x belonging to any of the intervals.

        All the intervals include the left end and exclude the right.
        """
        i = np.searchsorted(self.LR, x, side='right')
        cluster_no, in_clust = np.divmod(i, 2)
        cluster_no = np.where(in_clust, cluster_no, -1)
        return cluster_no


class OpenOpen(Interval):
    def __getitem__(self, x):
        """Querry for x belonging to any of the open intervals."""
        i = np.searchsorted(self.LR, x, side='left')
        cluster_no, in_clust = np.divmod(i, 2)
        # 'clip' fixes the problem with points right to max(R)
        # by changing the index from 2*len(L) to 2*len(L)-1.
        # This is ok, because these points have in_clust == 0 anyway.
        not_right_end = x < np.take(self.R, cluster_no, mode='clip')
        cluster_no = np.where(np.logical_and(in_clust, not_right_end), cluster_no, -1)
        return cluster_no


def test_non_overlapping_intervals():
    L = np.array([0, 10])
    R = np.array([1, 11])
    OC = OpenClosed(L, R)
    x = (-1, 0, .5, 1, 2, 10, 10.5, 11, 12)
    assert all(OC[x] == [-1,-1, 0, 0,-1,-1, 1, 1,-1])
    CO = ClosedOpen(L, R)
    assert all(CO[x] == [-1, 0, 0,-1,-1, 1, 1,-1,-1])
    OO = OpenOpen(L, R)
    assert all(OO[x] == [-1,-1, 0,-1,-1,-1, 1,-1,-1])



def get_intervals_np(X, max_diff=0.0, sorted=False):
    """Get left and right ends of the max-diff-net around points X.

    Args:
        X (iterable): points for which we need intervals.
        max_diff (float): half of the max distance between points in the net.
    Returns:
    A tuple of np.arrays with left and right ends of intervals.
    """
    if not sorted:
        X = np.sort(X)
    dXok = np.diff(X) >= max_diff * 2.0001
    Lidx = np.concatenate((np.array([True]), dXok))
    Ridx = np.concatenate((dXok, np.array([True])))
    return X[Lidx]-max_diff, X[Ridx]+max_diff

