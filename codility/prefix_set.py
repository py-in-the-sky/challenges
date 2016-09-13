"""
Prefix Set

https://codility.com/demo/take-sample-test/ps/

A is an array of integers.  Find the shortest prefix of A that contains all the
distinct integers in A.

E.g., solution([2, 2, 1, 0, 2]) == 3  # returns the last index of the prefix

Runtime: O(N)
Extra Space: O(N)
"""


def solution(A):
    distinct1 = set(A)
    distinct2 = set()
    prefix_idx = -1

    while len(distinct2) < len(distinct1):
        prefix_idx += 1
        distinct2.add(A[prefix_idx])

    return prefix_idx
