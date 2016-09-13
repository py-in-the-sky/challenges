"""
https://codility.com/programmers/task/perm_missing_elem/

Given array A of integers.  N = len(A).  Integers are distinct and taken from
range 1..(N+1), which means exactly one integer from 1..(N+1) is missing from
A.  Find the missing integer.

Runtime: O(N)
Extra Space: O(1)
"""


def solution(A):
    total1 = sum(xrange(1, len(A) + 2))  # sum of 1..(N+1)
    total2 = sum(A)
    return total1 - total2
