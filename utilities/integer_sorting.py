"""
Integer Sorting

See: https://courses.edx.org/courses/course-v1:ITMOx+I2CPx+3T2016/courseware/3e4889eff12145bbb546d72c531cf952/349ce46e9ae2498683924be9c1e4918f/

Integers bounded by 2^W, where W is word size (16, 32, or 64)

    shorts: 16
    integer: 32
    longs: 64

counting sort:
    given a small range of possible integers (e.g., ASCII alphabet)
    e.g., sort an ASCII string (256 possible distinct characters)

bucket sort:
    N key-value pairs
    keys are in [0, M), where M is small
    storage: array of lists
        array of length M
        each list is indexed in the array by the integer
        each list contains the values seen, in order, under that integer
            stable sorting of the different values that belong to the same key

radix sort:
    given N integer arrays, each of length L.
    bucket sort by the ith value for i in [L-1, L-2, ..., 0]
        runtime: runtime of bucket sort time L: O((N + M) * L)
        extra space: O(N + M)
"""


from collections import Counter, defaultdict
from functools import reduce


def counting_sort(A, ordered_keys):
    # Every element of A is in ordered_keys.
    counts = Counter(A)
    return [key for key in ordered_keys for _ in range(counts[key])]


def bucket_sort(A, ordered_keys, key=lambda x: x):
    # key maps elements of A onto ordered_keys.
    buckets = defaultdict(list)

    for elem in A:
        buckets[key(elem)].append(elem)

    return [val for key in ordered_keys for val in buckets[key]]


def radix_sort(A, ordered_keys):
    """Sort the elements of A lexicographically. All elements of A must have
    the same length. Each element of A must be composed of the elements from
    ordered_keys, and nothing else."""
    if not A:
        return []

    def _bucket_sort(A, index):
        return bucket_sort(A, ordered_keys, key=lambda A2: A2[index])

    L = len(A[0])
    assert all(len(a) == L for a in A)
    return reduce(_bucket_sort, reversed(range(L)), A)


def tests():
    from string import ascii_lowercase

    assert counting_sort([1, 0, 19, 18, 17, 5, 1], range(20)) == [0, 1, 1, 5, 17, 18, 19]
    assert counting_sort('poiawesaf', ascii_lowercase) == ['a', 'a', 'e', 'f', 'i', 'o', 'p', 's', 'w']

    assert bucket_sort([2, 4, -4, 4, 19, -18, -1, 1], range(-19, 20)) == [-18, -4, -1, 1, 2, 4, 4, 19]
    assert bucket_sort([2, 4, -4, 4, 19, -18, -1, 1], range(20), key=abs) == [-1, 1, 2, 4, -4, 4, -18, 19]

    assert radix_sort(['asdf', 'asde', 'aadz'], ascii_lowercase) == ['aadz', 'asde', 'asdf']

    print('tests pass!')
