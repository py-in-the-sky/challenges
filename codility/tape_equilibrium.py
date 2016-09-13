"""
https://codility.com/demo/take-sample-test/tape_equilibrium/

Runtime: O(N)
Extra Space: O(N)
"""


def solution(A):
    total = sum(A)
    running_total_from_left = A[0]
    min_diff = float('inf')

    for i in xrange(1, len(A)):
        right_half_total = total - running_total_from_left
        diff = abs(running_total_from_left - right_half_total)
        min_diff = min(min_diff, diff)
        running_total_from_left += A[i]

    return min_diff
