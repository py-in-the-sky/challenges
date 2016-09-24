"""
https://codility.com/programmers/task/min_avg_two_slice/

A slice is a sequence of contiguous elements..  We track `best_ending_at` along
the way and take the overall best one to be `best`.  For each index i of A, 
`best_ending_at` is the slice that has the smallest average of all slices that
end at i.  
"""


from __future__ import division
from collections import namedtuple


Slice = namedtuple('slice', 'avg len pos')


def solution(A):
    best = best_ending_at = Slice((A[0] + A[1]) / 2, 2, 0)

    for i in xrange(2, len(A)):
        candidate1 = Slice((A[i] + A[i-1]) / 2, 2, i-1)
        candidate2 = Slice(
            (best_ending_at.avg * best_ending_at.len + A[i]) / (best_ending_at.len + 1), 
            best_ending_at.len + 1, 
            best_ending_at.pos
        )
        best_ending_at = min(candidate1, candidate2)
        best = min(best, best_ending_at)

    return best.pos
