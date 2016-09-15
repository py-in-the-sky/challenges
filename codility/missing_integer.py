"""
https://codility.com/programmers/task/missing_integer/
"""


def solution(A):
    N = len(A)
    integers = set(A)
    return next(i for i in xrange(1, N+2) if i not in integers)
    # Since A contains N elements, by the pigeon-hole principle,
    # the smallest missing integer has to be in 1..(N+1)
