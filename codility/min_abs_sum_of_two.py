"""
https://codility.com/programmers/task/min_abs_sum_of_two/
"""


from bisect import bisect_left


def solution(A):
    if 0 in A:
        return 0
    elif all(a > 0 for a in A):
        return 2 * min(A)
    elif all(a < 0 for a in A):
        return -2 * max(A)
    else:
        neg, pos = sorted(a for a in A if a < 0), [a for a in A if a > 0]
        result = float('inf')

        for p in pos:
            i = bisect_left(neg, -p)
            smaller = min(abs(p + neg[j]) for j in (i, i-1) if 0 <= j < len(neg))
            result = min(result, smaller)

        return result
