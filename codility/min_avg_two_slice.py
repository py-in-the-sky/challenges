"""
https://codility.com/programmers/task/min_avg_two_slice/
"""


from __future__ import division
from collections import namedtuple


Slice = namedtuple('slice', 'avg len pos')


def solution(A):
    best = best_ending_at = Slice((A[0] + A[1]) / 2, 2, 0)

    for i in xrange(2, len(A)):
        length = best_ending_at.len + 1
        average = (best_ending_at.avg * best_ending_at.len + A[i]) / length
        candidate1 = Slice(average, length, best_ending_at.pos)
        candidate2 = Slice((A[i] + A[i-1]) / 2.0, 2, i-1)
        best_ending_at = min(candidate1, candidate2)
        best = min(best, best_ending_at)

    return best.pos
