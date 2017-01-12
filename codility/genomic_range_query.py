"""
https://codility.com/programmers/task/genomic_range_query/
"""


from collections import Counter


def solution(S, P, Q):
    # Instead of counters, could've also used four prefix-sum and four suffix-sum
    # arrays.  E.g., `pref_1` would just do a prefix sum across S, summing up
    # only the ones; `pref_2` would sum up only the twos; etc.
    values = {'A': 1, 'C': 2, 'G': 3, 'T': 4}
    S = tuple(values[char] for char in S)
    total_counts = Counter(S)
    pref = prefix_counts(S)
    suff = suffix_counts(S)

    def _min_impact_factor(p, q):
        slice_counts = {val: (count - pref[p][val] - suff[q][val]) 
                        for val,count in total_counts.iteritems()}
        return next(v for v in (1, 2, 3, 4) if v in slice_counts and slice_counts[v] > 0)

    return [_min_impact_factor(p, q) for p,q in zip(P, Q)]


def prefix_counts(A):
    result = [None] * len(A)
    result[0] = {val: 0 for val in (1, 2, 3, 4)}

    for i in xrange(1, len(A)):
        counts = result[i-1].copy()
        counts[A[i-1]] += 1
        result[i] = counts

    return result


def suffix_counts(A):
    result = [None] * len(A)
    result[-1] = {val: 0 for val in (1, 2, 3, 4)}

    for i in xrange(len(A)-2, -1, -1):
        counts = result[i+1].copy()
        counts[A[i+1]] += 1
        result[i] = counts

    return result
